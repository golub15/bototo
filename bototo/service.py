import logging

from aiogram.filters import Command, CommandObject

from aiogram.types import (
    Message
)

from bototo.bot import get_bot
from bototo.routers import main_router
from bototo.api import UserServiceProtocol

from .const import USER_SERVICE_KEY

logger = logging.getLogger(__name__)


#
# async def show_gui(
#         dialog_manager: DialogManager,
#         user_service: UserService,
#         state=MainSG.HELLO_STATE,
# ):
#     logger.warning("New stack")
#     await dialog_manager.start(MainSG.HELLO_STATE, mode=StartMode.NORMAL, show_mode=ShowMode.DELETE_AND_SEND)


# # обработчик ошибок
# @main_router.errors()
# async def bot_error_handler(event: ErrorEvent):
#     logger.exception(event.exception)
#     # await show_gui(dialog_manager, password_manager)


#
# async def setup_bot_commands(bot: Bot, commands: dict):
#     await bot.set_my_commands(
#         [
#             BotCommand(command=command, description=description)
#             for command, description in commands.items()
#         ],
#         scope=BotCommandScopeDefault(),
#     )


# @main_router.message(Command(commands=["menu", "start"]))
# async def start_gui(message: Message, dialog_manager: DialogManager, user_service: UserService):
#     await show_gui(dialog_manager, user_service)

# @main_router.message(Command(commands=["admin_panel"]))
# async def show_panel(
#         message: Message, command: CommandObject,
#         user_service: UserServiceProtocol
# ):
#     pass


@main_router.message(Command(commands=["admin"]))
async def make_admin(
        message: Message, command: CommandObject,
        **kwargs
):
    user_service: UserServiceProtocol = kwargs[USER_SERVICE_KEY]

    if command.args is not None and command.args == get_bot().settings.ADMIN_PASSWORD:
        await user_service.update_admin(new_status=True)
        # await setup_bot_commands(admin_commands)
        await message.answer(text="Вы теперь админ")
    else:
        if user_service.is_admin:
            await user_service.update_admin(new_status=False)
            await message.answer(text="Вы больше не админ")
        else:
            await message.answer(text="Неверный пароль")

# dp.update.outer_middleware.register(api_middleware)  # регистрация обработчика api

# main_router.include_router(account_dialog)
# main_router.include_router(group_dialog)
# main_router.include_router(settings_dialog)
# main_router.include_router(change_mp_dialog)
# main_router.include_router(help_dialog)
# main_router.include_router(account_share_dialog)
# main_router.include_router(mp_input_dialog) # it doesn't seem to be used
