import asyncio
from bot_instance import bot
from bot_handlers.user_handlers import user_router

from aiogram import Bot, Dispatcher
from aiogram.utils.markdown import hbold





def register_router(dp: Dispatcher) -> None: 
    """dispatcher processes msg and invoke msg handlers"""
    dp.include_router(user_router)



async def main() -> None : 
    # event loop & polling 
    dp = Dispatcher()
    register_router(dp)
 

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())