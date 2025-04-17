from aiogram.fsm.state import StatesGroup, State


class AdminPanelState(StatesGroup):
    MAIN_MENU = State()
    USER_BROADCAST = State()

    USER_ANALYTICS = State()
    BOT_SETTINGS = State

    INPUT_LANG_KEY = State()
    EDIT_TEXT_KEY = State()
