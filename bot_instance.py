from aiogram import Bot
from token_api import bot_token

bot = Bot(
    token= bot_token,
    parse_mode= 'HTML'
)