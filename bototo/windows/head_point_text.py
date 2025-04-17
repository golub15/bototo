from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text


class HeadPointText(Text):
    def __init__(self, when: WhenCondition = None):
        super().__init__(when=when)

    async def _render_text(
            self, data: dict, manager: DialogManager,
    ) -> str:
        # if manager.is_preview():
        #     return self.text.format_map(_FormatDataStub(data=data))
        return manager.dialog_data.get("header", "")
