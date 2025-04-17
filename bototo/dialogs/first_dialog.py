
from aiogram_dialog import Dialog, LaunchMode
from aiogram_dialog.widgets.text import Const

from ..states import MainSG
from ..windows.menu_point import MenuPoint
from ..user_service import UserService


# from app.bot.dialogs.iot_helper import account_checked, create_account
# from app.bot.states import *
# from app.bot.windows.input_forms import InputForm
# from app.bot.windows.menu_point import CLOSE_DIALOG, MenuPoint
# from app.sevices.manager import PasswordManager


async def getter(user_service: UserService, **kwargs):
    data = {
    }
    # data.update(await password_manager.get_user_info())

    return data


#
#
# async def group_checked(callback: CallbackQuery, widget: Any, manager: DialogManager, item: str):
#     await manager.start(GroupSG.MAIN_STATE, data={"uid": item})
#
#
# async def create_group(callback: CallbackQuery, button: Button, manager: DialogManager):
#     password_manager = manager.middleware_data["password_manager"]
#     group_uid = await password_manager.create_group()
#     # await manager.start(state=GroupSG.MAIN_STATE, data={"uid": group_uid})
#
#
# async def default_group_getter(password_manager: PasswordManager, **kwargs):
#     return {
#         "items": await password_manager.get_accounts_in_group(group_uid=None),
#     }
#
#
# async def shared_accounts_getter(password_manager: PasswordManager, **kwargs):
#     return {
#         "items": await password_manager.get_shared_accounts(),
#     }
#
#
# async def set_master_save(
#         input_data: str, dialog_manager: DialogManager, password_manager: PasswordManager, bot: Bot, **kwargs
# ):
#     assert 8 <= len(input_data) < 40, "Длина мастер пароля должна быть не менее 8 символов"
#
#     await bot.send_message(
#         password_manager.user.telegram_id,
#         f"Ваш мастер пароль: <code>{input_data}</code>" f"\n\n<b>Это сообщение напоминание, удалите его</b>",
#     )
#
#     await password_manager.create_or_update_MP(input_data)
#     await password_manager.welcome(flag=True)
#     await dialog_manager.switch_to(MainSG.MAIN_STATE)
#
#
# async def master(input_data: str, dialog_manager: DialogManager, password_manager: PasswordManager, **kwargs):
#     assert 1 < len(input_data) < 20, "Мастер пароль слишком мал"
#
#     await password_manager.create_or_update_MP(input_data)
#     await password_manager.welcome(flag=True)
#     await dialog_manager.switch_to(MainSG.MAIN_STATE)
#
#
# def have_shared(data: Dict, widget: Whenable, manager: DialogManager):
#     return data["users_shared_accounts_count"] > 0


main_dialog = Dialog(
    MenuPoint(
        Const(
            "✨ Привет новый пользователь"
        ),
        Const(" "),
        Const(
            "✨ 123"
        ),
        Const(" "),
        Const(
            "TEXT"
        ),
        Const(" "),
        Const("✅ <b>123</b>"),
        # SwitchTo(Const("Далее ➡ "), id="set_master", state=MainSG.MASTER_PASSWORD_STATE),
        state=MainSG.HELLO_STATE,
        getter=getter,
    ),
    launch_mode=LaunchMode.STANDARD,  #
)
