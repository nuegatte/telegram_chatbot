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
async def process_password_message(message: types.Message, state: FSMContext):
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



@user_router.message(Command("reply"))
async def cmd_reply(message: types.Message):
    """The function replies to your message"""

    await message.answer('Reply message replies! 😻', reply_markup= keyboard.reply_kb)


@user_router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    """The function answers dice to your message"""
    
    await message.answer_dice(emoji="🎲")


@user_router.message(Command("admin_info"))
async def cmd_admin_info(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        await message.answer("You are an admin.")
    else:
        await message.answer("You are not an admin.")


# @user_router.message(Command("start"))
# async def cmd_start(message: types.Message, config: BotConfig):
#     await message.answer(config.welcome_message, reply_markup= keyboard.ikb)

@user_router.message()
async def echo_message(message: types.Message):
    if "hi " in message.text.lower() or "hello" in message.text.lower() or "hai " in message.text.lower():
        await message.answer("Hello brother! How are you?")
    elif "bye" in message.text.lower() or " bai " in message.text.lower()  or "cya" in message.text.lower():
        await message.answer("Bye brother! See you soon!")
        sys.exit(0)
    else:
        await message.answer("Your message is not impactful enough for a special response.")


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


login_data = {
    "user1": "password1",
    "user2": "password2",
    # Add more users and passwords as needed
}
# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher


# Define the login data
LOGIN_DATA = {
    "user" : "123"
}

# # Define the login keyboard
# @user_router.message(Command("start")))
# async def send_login_menu(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup()
#     username_button = types.InlineKeyboardButton(text="Enter username", callback_data="username")
#     password_button = types.InlineKeyboardButton(text="Enter password", callback_data="password")
#     keyboard.row(username_button, password_button)
#     await message.answer("Please enter your login credentials.", reply_markup=keyboard)

# # Handle username and password input
# @user_router.callback_query(F.data)
# async def process_callback_query(callback_query: types.CallbackQuery):
#     data = callback_query.data
#     if data == "username":
#         await callback_query.message.answer(callback_query.from_user.id, "Enter your username:")
#         LOGIN_DATA['username'] = await bot.ask(callback_query.from_user.id, "username")
#     elif data == "password":
#         await bot.answer_callback_query(callback_query.id)
#         await callback_query.message.answer(callback_query.from_user.id, "Enter your password:")
#         LOGIN_DATA['password'] = await bot.ask(callback_query.from_user.id, "password")

#         # Check the login credentials
#         if LOGIN_DATA['username'] == "YOUR_USERNAME" and LOGIN_DATA['password'] == "YOUR_PASSWORD":
#             await callback_query.message.answer(callback_query.from_user.id, "Login successful!")
#         else:
#             await callback_query.message.answer(callback_query.from_user.id, "Invalid username or password.")





# Initialize bot

