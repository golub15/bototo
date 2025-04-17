from .api import BotManagerProtocol


def _get_bot(new: BotManagerProtocol = None) -> BotManagerProtocol:
    if new is not None:
        _get_bot.bot = new
    else:
        if not getattr(_get_bot, "bot", None):
            raise AttributeError("Not inited")
        else:
            return _get_bot.bot


def init_bot(new: BotManagerProtocol):
    return _get_bot(new)


def get_bot() -> BotManagerProtocol:
    return _get_bot()
