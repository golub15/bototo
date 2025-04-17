import logging
from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

from ..const import TEXT_DICT, EMBEDDED_TEXT_DICT, INVALID_TEXT_KEY, TRUE_LANG_CODE_KEY
from ..templates import render_template

from ..const import USER_SERVICE_KEY, MANAGER_KEY
from ..api import UserServiceProtocol, BotManagerProtocol
from jinja2.exceptions import TemplateNotFound

logger = logging.getLogger(__name__)


class JinjaByKey(Text):
    def __init__(self, key: str, use_lang: bool = True, when: WhenCondition = None):
        super().__init__(when=when)
        self.key = key
        self.use_lang = use_lang

    async def _render_text(
            self, data: Dict, manager: DialogManager,
    ) -> str:
        key = self.key
        if self.use_lang:
            key = f"{manager.middleware_data[TRUE_LANG_CODE_KEY]}/{self.key}"
        try:
            return render_template(key, data)
        except TemplateNotFound as e:
            logger.exception(e)
            return f"[Template not found: {key}]"


class TextByKey(Text):
    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.key = key

    async def _render_text(
            self, data: Dict, manager: DialogManager,
    ) -> str:
        return manager.middleware_data.get(TEXT_DICT, {}).get(self.key, INVALID_TEXT_KEY)


class EmbeddedTextByKey(Text):
    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.key = key

    async def _render_text(
            self, data: Dict, manager: DialogManager,
    ) -> str:
        return manager.middleware_data.get(EMBEDDED_TEXT_DICT, {}).get(self.key, INVALID_TEXT_KEY)
