from aiogram_dialog import DialogManager
from .api import UserServiceProtocol
from .const import USER_SERVICE_KEY


def is_admin(data, widget, manager: DialogManager):
    user: UserServiceProtocol = manager.middleware_data[USER_SERVICE_KEY]
    return user.is_admin
