from aiogram.filters import Command
from aiogram import Router, types

user_router = Router()

@user_router.message(Command('start'))
async def cmd_start(msg : types.Message) -> None: 
    # start command
    await msg.answer("hello <b>world<b>!")
