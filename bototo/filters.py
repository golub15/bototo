from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import Router
from bototo.const import ADMIN_ROUTER_NAME, USER_ROUTER_NAME
from .const import USER_SERVICE_KEY
from .api import UserServiceProtocol

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


class ShowGuiFilter(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message, event_router: Router, **kwargs) -> bool:
        if message.text in ["/start", "/menu"]:
            return True

        if kwargs["aiogd_context"] is None:
            msg = await message.answer("[]", reply_markup=ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text="[]")],
            ]))
            await msg.delete()
            return True

        return False


class AdminFilter(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message, event_router: Router, **kwargs) -> bool:
        user_service: UserServiceProtocol = kwargs[USER_SERVICE_KEY]

        if event_router.name == ADMIN_ROUTER_NAME and user_service.is_admin:
            return True
        else:
            return False
