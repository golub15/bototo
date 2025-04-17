from typing import *

from aiogram.enums import ContentType
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import *
from aiogram_dialog.widgets.utils import *
from aiogram_dialog.widgets.widget_event import ensure_event_processor

from .head_point_text import HeadPointText
from .text_by_key import EmbeddedTextByKey

CLOSE_DIALOG = State("close_dialog")


class MenuPoint(Window):
    def __init__(
            self,
            *widgets: WidgetSrc,
            state: State,
            back_state: Optional[State] = None,
            getter: GetterVariant = None,
            input_handler: Union[MessageHandlerFunc, WidgetEventProcessor, None] = None,
            back_handler: Union[OnClick, WidgetEventProcessor, None] = None,
            is_input=False,
            back_text=None,
            width=1,
            parse_mode: Optional[str] = "HTML",
            update_button: bool = False

    ):
        self._getter = ensure_data_getter(getter)
        self._input_handler = ensure_event_processor(input_handler)
        self._back_handler = ensure_event_processor(back_handler)
        self.is_input = is_input
        self.back_state = back_state
        self._kb_width = width

        widget_list = [HeadPointText(), *widgets]

        if back_state:
            back_btn_text = Const(back_text) if back_text else EmbeddedTextByKey("back")
            widget_list.append(Button(back_btn_text, id="back", on_click=self._back))

        if update_button:
            widget_list.append(Button(Const("🔃 Обновить"), id="refresh", on_click=self._refresh))

        widget_list.append(MessageInput(self._on_input, content_types=ContentType.TEXT))

        super().__init__(
            *widget_list,
            state=state,
            getter=self._get_data,
            parse_mode=parse_mode
        )

    async def _refresh(self, event: CallbackQuery, button: Button, manager: DialogManager):
        await event.answer()

    async def _on_input(self, event: Message, source: MessageInput, manager: DialogManager):
        await self._input_handler.process_event(event, source, manager)
        if self.is_input:
            pass
        else:
            await event.delete()

    async def go_back(self, manager: DialogManager, done_data: Any = None):
        if self.back_state == CLOSE_DIALOG:
            await manager.done(result=done_data)
        else:
            await manager.switch_to(self.back_state)

    async def _back(self, callback: CallbackQuery, button: Button, manager: DialogManager):
        await self._back_handler.process_event(callback, button, manager)
        await self.go_back(manager)

    async def _get_data(self, **kwargs):
        return await self._getter(**kwargs)
