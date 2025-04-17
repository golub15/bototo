import typing
from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol
from datetime import datetime
from pydantic import BaseModel


class UserDbData(BaseModel):
    id: int
    tg_id: int
    settings: dict
    welcome: bool
    created_at: datetime
    is_admin: bool
    full_name: str | None = None
    username: str | None = None


class DbProtocol(Protocol):

    async def get_or_create_user(self, tg_user_id: int) -> typing.Tuple[UserDbData, bool]:
        """

        :param tg_user_id:
        :return: model, is existing
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, bot_user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def update_admin(self, bot_user_id: int, new_status: bool):
        raise NotImplementedError

    @abstractmethod
    async def update_user_data(self, bot_user_id: int, full_name: str | None, username: str | None):
        raise NotImplementedError

    @abstractmethod
    async def count_all_user(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_users_filtered(self, is_admin: bool) -> list[UserDbData]:
        raise NotImplementedError
