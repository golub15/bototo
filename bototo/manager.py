import os
from abc import ABC
from typing import Optional, Dict, Any

import asyncio
import logging

from aiogram import Dispatcher, Bot, Router, exceptions
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import Message, Update, BotCommand, BotCommandScopeDefault, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton

from aiogram.fsm.state import State
from aiogram.filters import Command, StateFilter

from aiogram_dialog import DialogManager, StartMode, ShowMode

from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent

from .routers import main_router, admin_router, user_router
from .const import DB_USER_MODEL_KEY, MANAGER_KEY, USER_SERVICE_KEY, TEXT_DICT, EMBEDDED_TEXT_DICT, TRUE_LANG_CODE_KEY
from .user_service import UserServiceImpl, DefaultUserServiceBuilder
from .admin_panel.analytics import admin_panel
from .admin_panel.state import AdminPanelState
from .api import FluentStorageProtocol, BotManagerProtocol, DbProtocol, BototoSettings, UserServiceBuilder
from .service import *
from .filters import AdminFilter, ShowGuiFilter

from .fluent_storage.file import FluentStorageFile

logger = logging.getLogger(__name__)


async def start_gui(message: Message, dialog_manager: DialogManager, bot_manager: BotManagerProtocol):
    await dialog_manager.start(bot_manager.main_menu_state, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.DELETE_AND_SEND)


async def start_admin_gui(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AdminPanelState.MAIN_MENU, mode=StartMode.RESET_STACK, show_mode=ShowMode.EDIT)


class BototoManager(BotManagerProtocol):
    # broadcast_messages: asyncio.Queue

    def __init__(
            self, settings: BototoSettings,
            db_protocol: DbProtocol,
            fsm_storage: Optional[BaseStorage],
            main_routers: list[Router] = None,
            admin_routers: list[Router] = None,
            main_menu_state: State = None,
            user_service_builder: UserServiceBuilder = None,
            user_fluent_storage: FluentStorageProtocol = None,
            embedded_fluent_storage: FluentStorageProtocol = None,
            default_lang_code="en"
    ):

        if user_service_builder is None:
            user_service_builder = DefaultUserServiceBuilder()

        if embedded_fluent_storage is None:
            self._embedded_fluent_storage = FluentStorageFile(
                file_path=os.path.join(os.path.dirname(__file__), "embedded_texts/lang_all.json")
            )

        self._db_protocol = db_protocol
        self._user_fluent_storage = user_fluent_storage

        self._main_menu_state = main_menu_state
        self.default_lang_code = default_lang_code

        self._user_service_impl = user_service_builder
        self._settings = settings

        self.broadcast_messages = asyncio.Queue()

        self._bot = Bot(
            token=self.settings.TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        self._dp = Dispatcher(
            storage=fsm_storage, events_isolation=SimpleEventIsolation()
        )

        if main_menu_state is not None:
            main_router.message.register(start_gui, ShowGuiFilter())

        self.dp.message.outer_middleware.register(self._manager_middleware)
        self.dp.callback_query.outer_middleware.register(self._manager_middleware)

        self.dp.include_router(main_router)  # router для обработки сообщений и диалогов

        admin_router.message.filter(AdminFilter())
        # user_router.message.filter(AdminFilter())

        if main_routers is not None:
            for r in main_routers:
                user_router.include_router(r)

        if admin_routers is not None:
            for r in admin_routers:
                admin_router.include_router(r)

        admin_router.include_router(admin_panel)
        admin_router.message.register(start_admin_gui, Command(commands=["panel"]))

        main_router.include_router(admin_router)
        main_router.include_router(user_router)

        setup_dialogs(self.dp)  # регистрация диалогов aiogram-dialog

    async def _manager_middleware(self, handler, event: Update, data: Dict[str, Any]) -> Any:
        logger.debug("Bototo manger middleware pass")

        data[MANAGER_KEY] = self
        # data[DB_USER_MODEL_KEY] = self.db_user_model

        user_service = await self._user_service_impl.build(data["event_from_user"], self.db_protocol)
        data[USER_SERVICE_KEY] = user_service

        lang_code = user_service.lang_code
        if lang_code is not self.settings.SUPPORT_LANG_CODES:
            lang_code = self.settings.DEFAULT_LANG_CODE

        data[TRUE_LANG_CODE_KEY] = lang_code

        if self.user_fluent_storage:
            data[TEXT_DICT] = self.user_fluent_storage.get_dict_for_lang(lang_code)

        data[EMBEDDED_TEXT_DICT] = self.embedded_fluent_storage.get_dict_for_lang(lang_code)

        try:
            return await handler(event, data)
        except UnknownIntent:
            if isinstance(event, CallbackQuery):
                await event.answer(data[EMBEDDED_TEXT_DICT]["old_msg"], show_alert=True)
        except Exception as e:
            logger.exception(e)

    async def broadcast_msg_send_task(self):
        while True:
            chat_id, text = await self.broadcast_messages.get()
            await self.send_message_to_user(user_id=chat_id, text=text)

    async def send_to_admins(self, msg: str):
        user_list = await self.db_protocol.get_users_filtered(is_admin=True)
        tg_id_list = [x.tg_id for x in user_list]

        for tg_id in tg_id_list:
            logger.warning(f"Send -{tg_id, msg}")
            await self.broadcast_messages.put((tg_id, msg))

    async def send_message_to_user(
            self,
            user_id: int,
            text: str,
            disable_notification: bool = False
    ) -> bool:

        attempt = 0
        while attempt < 10:
            try:
                await self.bot.send_message(
                    user_id,
                    text,
                    disable_notification=disable_notification
                )
            except exceptions.TelegramForbiddenError:
                logging.error(f"Target [ID:{user_id}]: blocked by user")
                return False
            except exceptions.TelegramRetryAfter as e:
                logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. ")
                await asyncio.sleep(e.retry_after)
            except exceptions.TelegramAPIError:
                logging.exception(f"Target [ID:{user_id}]: failed")
                await asyncio.sleep(60)
            else:
                logging.info(f"Target [ID:{user_id}]: success")
                return True

    async def setup_bot_commands(self, commands_dict: dict[str, str]):
        await self.bot.set_my_commands(
            [
                BotCommand(command=command, description=description)
                for command, description in commands_dict.items()
            ],
            scope=BotCommandScopeDefault(),
        )

    @property
    def user_fluent_storage(self) -> FluentStorageProtocol:
        return self._user_fluent_storage

    @property
    def embedded_fluent_storage(self) -> FluentStorageProtocol:
        return self._embedded_fluent_storage

    @property
    def db_protocol(self) -> DbProtocol:
        return self._db_protocol

    @property
    def main_menu_state(self) -> State:
        return self._main_menu_state

    @property
    def settings(self) -> BototoSettings:
        return self._settings

    @property
    def bot(self) -> Bot:
        return self._bot

    @property
    def dp(self) -> Dispatcher:
        return self._dp

    async def start(self, as_bg_task: bool = False):
        notification_task = asyncio.create_task(self.broadcast_msg_send_task())

        await self.embedded_fluent_storage.load()
        if self.user_fluent_storage:
            await self.user_fluent_storage.load()

        if as_bg_task:
            polling_task = asyncio.create_task(
                self.dp.start_polling(
                    self.bot,
                    handle_signals=False
                )
            )
        else:
            await self.dp.start_polling(self.bot)

    async def shutdown(self):
        await self.dp.stop_polling()
