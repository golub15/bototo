from aiogram.types import User
from .api import UserServiceProtocol, UserServiceBuilder, UserDbData, DbProtocol


#
# @classmethod
# async def get_by_telegram(cls, tg_user: User, db_protocol: DbProtocol) -> "UserServiceProtocol":
#     user_data, is_exist = await db_protocol.get_or_create_user(tg_user.id)
#
#     if not is_exist or user_data.full_name is None:
#         await db_protocol.update_user_data(
#             user_data.id,
#             full_name=tg_user.full_name,
#             username=tg_user.username
#         )
#
#     return UserServiceImpl(
#         db_protocol=db_protocol,
#         tg_user=tg_user,
#         user_data=user_data
#     )

class DefaultUserServiceBuilder(UserServiceBuilder):
    async def build(self, tg_user: User, db_protocol: DbProtocol) -> "UserServiceProtocol":
        user_data, is_exist = await db_protocol.get_or_create_user(tg_user.id)

        if not is_exist or user_data.full_name is None:
            await db_protocol.update_user_data(
                user_data.id,
                full_name=tg_user.full_name,
                username=tg_user.username
            )

        return UserServiceImpl(
            db_protocol=db_protocol,
            tg_user=tg_user,
            user_data=user_data
        )


class UserServiceImpl(UserServiceProtocol):

    def __init__(self, db_protocol: DbProtocol, tg_user: User, user_data: UserDbData):
        self._db_protocol: DbProtocol = db_protocol
        self._tg_user = tg_user
        self._user_data = user_data

    async def update_admin(self, new_status: bool):
        await self._db_protocol.update_admin(self._user_data.id, new_status)

    @property
    def is_admin(self):
        return self._user_data.is_admin

    @property
    def lang_code(self) -> str:
        return self._tg_user.language_code

    @property
    def data(self) -> UserDbData:
        return self._user_data

    async def delete(self):
        await self._db_protocol.delete_user(self._user_data.id)
