from aiogram import Router, types , F
from aiogram.types import CallbackQuery
from aiogram.filters import Command
# from fractions import Fraction as F
# from aiogram.handlers import CallbackQueryHandler
# from aiogram.filters.callback_data import CallbackData
from bot.config import BotConfig
from bot import keyboard
import sys, logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram.filters.state import StateFilter
from random import randint

user_router = Router()



# Define the login data
LOGIN_DATA = {}

# Define the login states
class LoginStates(StatesGroup):
    username = State()
    password = State()

# Initialize the FSM dispatcher


# Define the message handler for the "/start" command
@user_router.message(Command("start"))
async def cmd_start(message: types.Message):
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text="Enter username", callback_data="username"),
        types.InlineKeyboardButton(text="Enter password", callback_data="password")
    ]
    ])
    await message.answer("Please enter your login credentials.", reply_markup=keyboard)

# Define the callback query handler for the login buttons
@user_router.callback_query(StateFilter(LoginStates.username))
async def process_username_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(callback_query.from_user.id, "Enter your username:")
    await state.set_state(LoginStates.username)

@user_router.message(StateFilter(LoginStates.username))
async def process_username_message(message: types.Message, state: FSMContext):
    LOGIN_DATA['username'] = message.text
    await state.set_state(LoginStates.password)
    await message.answer(message.from_user.id, "Enter your password:")

@user_router.callback_query(StateFilter(LoginStates.password))
async def process_password_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(callback_query.from_user.id, "Enter your password:")
    await state.set_state(LoginStates.password)

@user_router.message(StateFilter(LoginStates.password))
async def process_password_message(message: types.Message):
    LOGIN_DATA['password'] = message.text
    # Check the login credentials
    sample_credentials = {
    "user1": "pass1",
    "user2": "pass2",
    "user3": "pass3"
    }
    if LOGIN_DATA['username'] in sample_credentials and LOGIN_DATA['password'] == sample_credentials[LOGIN_DATA['username']]:
        await message.answer(message.from_user.id, "Login successful!")
    else:
        await message.answer(message.from_user.id, "Invalid username or password.")


# reply menu 
@user_router.message(Command("reply"))
async def cmd_reply(message: types.Message):
    """The function replies to your message"""

    await message.answer('Reply message replies! 😻', reply_markup= keyboard.reply_kb)

# dice emoji
@user_router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    """The function answers dice to your message"""
    
    await message.answer_dice(emoji="🎲")

# admin infos 
@user_router.message(Command("admin_info"))
async def cmd_admin_info(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        await message.answer("You are an admin.")
    else:
        await message.answer("You are not an admin.")



#reply random number generator 
@user_router.message(Command("random"))
async def random(message : types.Message):
    def rand():
        start = 10 ** (6 -1)
        end = (10**6)-1
        return randint(start, end)
    num = rand()
    await message.answer(f"The random 6  digits are {str(num)}")


#respond to certain text in messages
@user_router.message()
async def echo_message(message: types.Message):
    if "hi" in message.text.upper() or "hello" in message.text.lower() or "hai " in message.text.lower():
        await message.answer("Hello brother! How are you?")
    elif "bye" in message.text.lower() or " bai " in message.text.lower()  or "cya" in message.text.lower():
        await message.answer("Bye brother! See you soon!")
        sys.exit(0)
    elif "nice" in message.text.lower():
        await message.answer("nice balls bro lol!")
        
    else:
        await message.answer("Your message is not impactful enough for a special response.")




#inline reply/callback 
@user_router.callback_query(F.data == "hello")
async def testingbro(query : CallbackQuery,config: BotConfig):
    await query.message.answer('LESGOOOOOOOOO')
    await cmd_start(query.message, config)

@user_router.callback_query(F.data== "hello1")
async def testingbro(query : CallbackQuery,config: BotConfig):
    await query.message.answer('This is the 2nd inline button lesgooooooo')
    await cmd_admin_info(query.message, config)


@user_router.callback_query(F.data == "hello2")
async def testingbro(query : CallbackQuery):
    await query.message.answer('LESGOOOOOOOOO 3rd inline !!!!!!')
    await cmd_reply(query.message)



# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher





# Initialize bot

