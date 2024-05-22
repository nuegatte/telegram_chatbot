from aiogram import Router, types , F
from aiogram.types import CallbackQuery
from aiogram.filters import Command, CommandObject
from bot.config import BotConfig
from bot import keyboard
import sys, logging

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from random import randint

user_router = Router()

# finite state class
class RepeatState(StatesGroup):
    waiting_for_input = State()

"""
commands

start - start the bot 
repeat - uninterrupted repeat msg
reply - reply menu 
dice - dice emoji
admin_info - yes
random - rnadom 6 digit number


"""

# Define the message handler for the "/start" command
@user_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Welcome, fellow tutor!", reply_markup=keyboard.subject_ikb)

@user_router.callback_query(F.data == "sub_input")
async def sub_input(call: CallbackQuery, state : FSMContext):
    await call.message.edit_text("Enter the subject name:")
    await state.set_state(RepeatState.waiting_for_input)
    await state.update_data(message=call)

@user_router.message(RepeatState.waiting_for_input)
async def sub_output(message: types.Message, state: FSMContext):
    await state.clear()
    def rand():
        start = 10 ** (6 -1)
        end = (10**6)-1
        return randint(start, end)
    num = rand()
    await message.answer(f"Your subject name is: {message.text}, code : ||{str(num)}||", parse_mode="MarkdownV2")




#  uninterrupted service example : repeat message
@user_router.message(Command("repeat"))
async def repeat(message: types.Message, state: FSMContext):
    await message.answer("Tell me something and I will repeat it!")
    await message.answer("Enter your message:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RepeatState.waiting_for_input)
    await state.update_data(message=message)

# applying the repeat state
@user_router.message(RepeatState.waiting_for_input)
async def process_input(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f"||{message.text}||", parse_mode="MarkdownV2")

#####




@user_router.callback_query(F.data == "hello2")
async def testingbro(query : CallbackQuery):
    await query.message.answer('LESGOOOOOOOOO 3rd inline !!!!!!')
    await cmd_reply(query.message)

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





#respond to certain text in messages
@user_router.message()
async def echo_message(message: types.Message):
    if "hi" in message.text.upper() or "hello" in message.text.lower() or "hai " in message.text.lower():
        await message.answer("Hello brother! How are you?")
    elif "bye" in message.text.lower() or " bai " in message.text.lower()  or "cya" in message.text.lower():
        await message.answer("Bye brother! See you soon!")
        await message.answer("Bot process ended. Please restart via VS code.")
        sys.exit(0)
    elif "nice" in message.text.lower():
        await message.answer("nice balls bro lol!")
        





#inline reply/callback 
@user_router.callback_query(F.data == "hello")
async def testingbro(query : CallbackQuery,config: BotConfig):
    await query.message.answer('LESGOOOOOOOOO')
    await cmd_start(query.message, config)

@user_router.callback_query(F.data== "hello1")
async def testingbro(query : CallbackQuery,config: BotConfig):
    await query.message.answer('This is the 2nd inline button lesgooooooo')
    await cmd_admin_info(query.message, config)






# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher





# Initialize bot

