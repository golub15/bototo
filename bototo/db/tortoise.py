import typing

from ..api.db_protocol import DbProtocol, UserDbData

from tortoise.models import Model
from tortoise import fields


class OrmUserBot(Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField()
    full_name = fields.CharField(default="", max_length=255)
    username = fields.CharField(default="", max_length=255)

    settings = fields.JSONField(default={})
    welcome = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    admin = fields.BooleanField(default=False)

    class Meta:
        abstract = True


def _to_db_user_data(user: OrmUserBot) -> UserDbData:
    return UserDbData(
        id=user.id,
        tg_id=user.telegram_id,
        full_name=user.full_name,
        is_admin=user.admin,
        settings=user.settings,
        welcome=user.welcome,
        created_at=user.created_at,
    )


class TortoiseDb(DbProtocol):
    user_model: OrmUserBot

    def __init__(self, user_model: [OrmUserBot]):
        self.user_model = user_model

    async def count_all_user(self) -> int:
        return await self.user_model.all().count()

    async def get_users_filtered(self, is_admin: bool) -> list[UserDbData]:
        orm_users = await self.user_model.filter(admin=is_admin).all()
        return [_to_db_user_data(x) for x in orm_users]

    async def delete_user(self, bot_user_id: int):
        user = await self.user_model.get(id=bot_user_id)
        await user.delete()

    async def get_or_create_user(self, tg_user_id: int) -> typing.Tuple[UserDbData, bool]:
        user, is_exist = await self.user_model.get_or_create(telegram_id=tg_user_id)
        return _to_db_user_data(user), is_exist

    async def update_user_data(self, bot_user_id: int, full_name: str | None, username: str | None):
        await self.user_model.filter(id=bot_user_id).update(full_name=full_name, username=username)

    async def update_admin(self, bot_user_id: int, new_status: bool):
        await self.user_model.filter(id=bot_user_id).update(admin=new_status)
