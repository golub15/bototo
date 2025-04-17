
import asyncio
from typing import *

from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *
from aiogram_dialog.widgets.utils import *

from .menu_point import MenuPoint


class ConfirmForm(MenuPoint):
    def __init__(
            self,
            *widgets: WidgetSrc,
            state: State,
            back_state: Optional[State] = None,
            input_done=None,
            form_id: str = "confirm_form",
    ):
        self._input_done = input_done
        super().__init__(
            *widgets,
            Button(Const("✅ Да"), id=form_id, on_click=self._confirm_done),
            back_state=back_state,
            state=state,
            back_text="❌ Отмена",
        )

    async def _confirm_done(self, callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        dialog_manager.middleware_data["callback"] = callback
        try:
            await self._input_done(**dialog_manager.middleware_data)
        except (ValueError, AssertionError) as e:
            await callback.answer(f"❌ {e}", show_alert=True)
        except Exception as e:
            await callback.answer(f"❌ Фатальная ошибка: {e}", show_alert=True)


class InputForm(MenuPoint):
    def __init__(
            self,
            *widgets: WidgetSrc,
            state: State,
            back_state: Optional[State] = None,
            next_state: Optional[State] = None,
            done_state: Optional[State] = None,
            input_done=None,
            form_id: str = "save_data",
            use_fid=False,
            do_empty=False,
            confirm_btn=True,
            secret_field=False,
    ):
        """
        :param widgets:
        :param state:
        :param back_state:
        :param next_state:
        :param done_state:
        :param input_done:
        :param form_id:
        :param use_fid:
        :param do_empty: it is allowed to leave the  field is empty
        :param confirm_btn: add the button for confirming
        """
        self._input_done = input_done
        self._next_state = next_state
        self._done_state = done_state
        self._form_id = form_id
        self._confirm_btn = confirm_btn

        self.dict_data_key = form_id if use_fid else "input_data"

        if do_empty:
            widgets += (
                Button(
                    Const("🚫 сделать пустым"),
                    id="do_empty",
                    on_click=self._input_checker,
                ),
            )
        if confirm_btn:
            widgets += (
                Button(
                    Const("💾 потвердить"),
                    id=form_id,
                    on_click=self._input_checker,
                    when="input_data",
                ),
            )

        widgets += (Const(" "),)

        if not secret_field:
            widgets += (Format("➡ <code>{input_data}</code>", when="input_data"),)
        else:
            pass
            # widgets += (Const("➡ <code>******</code>"),)

        super().__init__(
            *widgets,
            Const(" "),
            back_state=back_state,
            state=state,
            back_handler=self.on_back,
            input_handler=self.on_input,
            getter=self.form_data_getter,
            is_input=True,
        )

    async def form_data_getter(self, dialog_manager: DialogManager, **kwargs):
        data = {}
        if self.dict_data_key in dialog_manager.dialog_data:
            data["input_data"] = dialog_manager.dialog_data[self.dict_data_key]

        return data

    async def on_input(self, event: Message, source: MessageInput, dialog_manager: DialogManager):
        dialog_manager.dialog_data[self.dict_data_key] = event.text
        if not self._confirm_btn:
            dialog_manager.middleware_data["input_data"] = dialog_manager.dialog_data.get(
                self.dict_data_key, ""
            )
            info, show_alert = await self.input_checker(dialog_manager)
            if info:
                pass
                # TODO: Change it
                # await show_msg(
                #     info,
                # )

    async def on_back(self, callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        if self.dict_data_key in dialog_manager.dialog_data:
            del dialog_manager.dialog_data[self.dict_data_key]

    async def _input_checker(self, callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        dialog_manager.middleware_data["input_data"] = ""
        if button.widget_id != "do_empty":
            dialog_manager.middleware_data["input_data"] = dialog_manager.dialog_data.get(
                self.dict_data_key, ""
            )
        info, show_alert = await self.input_checker(dialog_manager)
        await callback.answer(info, show_alert=show_alert)

    async def input_checker(self, dialog_manager: DialogManager):
        try:
            dialog_manager.middleware_data["form_id"] = self._form_id

            ret_data = "", False
            if asyncio.iscoroutinefunction(self._input_done):
                info_str = await self._input_done(**dialog_manager.middleware_data)
                if isinstance(info_str, str) and info_str:
                    ret_data = info_str, False

            if self._next_state is not None:
                await dialog_manager.switch_to(self._next_state)
            else:
                if self._done_state:
                    await dialog_manager.switch_to(state=self._done_state)
                else:
                    await self.go_back(
                        dialog_manager,
                        done_data={self.dict_data_key: dialog_manager.middleware_data["input_data"]},
                    )
            return ret_data
        except (AssertionError, ValueError) as msg:
            return f"❌ {msg}", True
        except Exception as e:
            return f"❌ Фатальная ошибка: {e}", True
