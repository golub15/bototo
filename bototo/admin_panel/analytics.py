# @admin_router.message(F.text == AdminMenuText.users)
# async def user_stats(message: Message,
#                      state: FSMContext,
#                      user_service: UserService,
#                      text: BotTexts,
#                      bot: Bot):
#     users = await User.all().values_list("id", "full_name", "created_at", "info")
#
#     users_arr = []
#     for user_id, full_name, created_at, info in users:
#         created_at += datetime.timedelta(hours=+5)
#         user_row = f"{user_id} | {full_name} | {info['username']} | {created_at.strftime('%d.%m.%y %H:%M:%S')}"
#         users_arr.append(user_row)
#
#     user_t = "\n".join(users_arr)
#     text = f"Пользователи\n\n{user_t}"
#     await message.answer(text=text)
import logging
from operator import itemgetter

from bototo.windows import MenuPoint, InputForm

from aiogram.types import Message

from aiogram_dialog import DialogManager, Dialog
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *
from ..windows.text_by_key import EmbeddedTextByKey
from aiogram_dialog.widgets.input import MessageInput

from ..const import TEXT_DICT
from ..bot import get_bot
from .state import AdminPanelState
from ..routers import admin_router

logger = logging.getLogger(__name__)


async def lang_key_text_getter(dialog_manager: DialogManager, **kwargs):
    try:
        split_text = dialog_manager.dialog_data["lang_key"].split("/")
        lang_code = split_text[0]
        lang_key = split_text[1]

        return {
            "text": dialog_manager.middleware_data[TEXT_DICT][lang_code][lang_key]
        }
    except KeyError:
        return {
            "key_error": True
        }


async def input_lang_keu_handler(
        message: Message,
        widget: MessageInput,
        manager: DialogManager,
):
    try:

        split_text = manager.dialog_data["lang_key"].split("/")
        lang_code = split_text[0]
        lang_key = split_text[1]

        if message.text is not None:
            await get_bot().user_fluent_storage.edit_key_and_save(
                lang_code,
                lang_key,
                message.text
            )
    except Exception as e:
        logger.exception(e)
        await message.answer("❌")


admin_panel = Dialog(
    MenuPoint(
        Const("Управление ботом"),
        SwitchTo(EmbeddedTextByKey("ch_translate"), id="edit_lang", state=AdminPanelState.INPUT_LANG_KEY),
        SwitchTo(EmbeddedTextByKey("user_broadcast"), id="ub", state=AdminPanelState.USER_BROADCAST),
        state=AdminPanelState.MAIN_MENU
    ),
    InputForm(
        EmbeddedTextByKey("langs"),
        state=AdminPanelState.INPUT_LANG_KEY,
        next_state=AdminPanelState.EDIT_TEXT_KEY,
        form_id="lang_key",
        use_fid=True,
        back_state=AdminPanelState.MAIN_MENU,

    ),
    MenuPoint(
        EmbeddedTextByKey("edit_lang_key"),
        EmbeddedTextByKey("key_error", when="key_error"),
        Format("{text}", when="text"),
        is_input=True,
        input_handler=input_lang_keu_handler,
        state=AdminPanelState.EDIT_TEXT_KEY,
        getter=lang_key_text_getter,
        back_state=AdminPanelState.MAIN_MENU
    ),
    MenuPoint(
        EmbeddedTextByKey("user_bc_about"),
        EmbeddedTextByKey("key_error", when="key_error"),
        Format("{text}", when="text"),
        is_input=True,
        input_handler=input_lang_keu_handler,
        state=AdminPanelState.USER_BROADCAST,
        getter=lang_key_text_getter,
        back_state=AdminPanelState.MAIN_MENU
    )
)
