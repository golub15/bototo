from aiogram import Router
from bototo.const import ADMIN_ROUTER_NAME, USER_ROUTER_NAME


main_router = Router()
admin_router = Router(name=ADMIN_ROUTER_NAME)
user_router = Router(name=USER_ROUTER_NAME)


