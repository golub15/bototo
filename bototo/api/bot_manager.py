import datetime
from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol
from .fluent_storage import FluentStorageProtocol
from .db_protocol import DbProtocol
from .settings import BototoSettings

from aiogram import Bot, Dispatcher

from aiogram.fsm.state import State


class BotManagerProtocol(Protocol):

    @abstractmethod
    def start(self, as_bg_task: bool = False):
        raise NotImplementedError

    @abstractmethod
    def shutdown(self):
        raise NotImplementedError

    @abstractmethod
    async def send_message_to_user(
            self,
            user_id: int,
            text: str,
            disable_notification: bool = False
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def send_to_admins(self, msg: str):
        raise NotImplementedError

    @property
    def user_fluent_storage(self) -> FluentStorageProtocol:
        raise NotImplementedError

    @property
    def embedded_fluent_storage(self) -> FluentStorageProtocol:
        raise NotImplementedError

    @property
    def db_protocol(self) -> DbProtocol:
        raise NotImplementedError

    @property
    def settings(self) -> BototoSettings:
        raise NotImplementedError

    @property
    def main_menu_state(self) -> State:
        raise NotImplementedError

    @property
    def bot(self) -> Bot:
        raise NotImplementedError

    @property
    def dp(self) -> Dispatcher:
        raise NotImplementedError
