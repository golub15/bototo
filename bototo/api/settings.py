from pydantic import BaseModel


class BototoSettings(BaseModel):
    TOKEN: str
    USE_WEBHOOK: bool = False
    ADMIN_PASSWORD: str
    TEMPLATES_DIR: str | None = None
    SUPPORT_LANG_CODES: list[str]
    DEFAULT_LANG_CODE: str
