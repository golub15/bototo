import datetime
from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from aiogram.types import User
from .db_protocol import DbProtocol, UserDbData


class UserServiceBuilder(Protocol):
    @abstractmethod
    async def build(self, tg_user: User, db_protocol: DbProtocol) -> "UserServiceProtocol":
        raise NotImplementedError


class UserServiceProtocol(Protocol):

    @abstractmethod
    async def update_admin(self, new_status: bool):
        raise NotImplementedError

    @property
    def lang_code(self) -> str:
        raise NotImplementedError

    @property
    def is_admin(self) -> bool:
        raise NotImplementedError

    @property
    def data(self) -> UserDbData:
        raise NotImplementedError

    @abstractmethod
    async def delete(self):
        pass
