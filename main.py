import asyncio 
from aiogram import Dispatcher
from bot_instance import bot

from bot.bot_handlers.user_handlers import user_router
from bot.bot_handlers.group_handlers import group_router
from bot.config import BotConfig


def register_routers(dp: Dispatcher) -> None:
    """Registers routers"""

    dp.include_routers(user_router, group_router)



async def main() -> None:
    """The main function which will execute our event loop and start polling."""
    
    config = BotConfig(
        admin_ids=[ 6749403874], 
        # admin_ids=[373468118, 6749403874], 
        welcome_message="Welcome to our Python Bot!"
        )


    dp = Dispatcher()
    dp["config"] = config

    register_routers(dp)

    await dp.start_polling(bot) #bot proceeds polling




# main 
if __name__ == "__main__":
    asyncio.run(main())
