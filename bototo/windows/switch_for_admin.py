from typing import Any, Optional

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery

from aiogram_dialog.api.entities import ChatEvent, Data, ShowMode, StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd.button import Button, OnClick
from aiogram_dialog.widgets.text import Const, Text
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor
from aiogram_dialog.widgets.kbd.state import EventProcessorButton

from ..const import USER_SERVICE_KEY
from ..api import UserServiceProtocol


class SwitchForAdmin(EventProcessorButton):
    def __init__(
            self,
            text: Text,
            id: str,
            state: State,
            on_click: Optional[OnClick] = None,
            when: WhenCondition = None,
            show_mode: Optional[ShowMode] = None,
    ):
        super().__init__(
            text=text, on_click=self._on_click,
            id=id, when=when,
        )
        self.text = text
        self.user_on_click = on_click
        self.state = state
        self.show_mode = show_mode

    async def _on_click(
            self, callback: CallbackQuery, button: Button,
            manager: DialogManager,
    ):
        if self.user_on_click:
            await self.user_on_click(callback, self, manager)
        user_service: UserServiceProtocol = manager.middleware_data[USER_SERVICE_KEY]

        if user_service.is_admin:
            await manager.switch_to(self.state, show_mode=self.show_mode)
        else:
            await callback.answer("Access forbiden 😀 (secret value)")
