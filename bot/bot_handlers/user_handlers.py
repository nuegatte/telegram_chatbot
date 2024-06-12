from aiogram import Router, types , F
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from bot.config import BotConfig
from bot import keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from random import randint
from ..firebase.fbauth import db
import sys, logging
import asyncio


# finite state class
# sets state to prevent interruption from other commands/responds
class States(StatesGroup):
    user_state = State()
    default = State()

class tutor(States):
    mode = State()





# Set up logging, show message handling in real time
logging.basicConfig(level=logging.INFO)



"""
commands

perms - check permissions
check_subjects - check subject list
restricted - check restrict
testing - testing the modes
start - start the bot 
repeat - uninterrupted repeat msg
admin_info - yes
stop - stop process
random - random 6 digit number


"""

# @user_router.message(Command("start"))
# async def startup(message: types.Message, state : FSMContext):
#     userID = message.from_user.id
#     username = message.from_user.username
    
#     userdata = {
#         "UserID" : userID,
#         "Username" : username,
#         "tutor" : False,
#     }

#     check_user = db.child("users").get()

#     if check_user.each():
#         await message.answer("Welcome.")

#         await state.set_state(States.default)

#     else: 
#         db.child("users").child(userID).set(userdata)
#         await state.set_state(States.default)
#         await message.answer(f"Welcome to Tutor Bot, {str(username)}! I'm here to help you with your studies.")
class testrouter (Router):
    router = sub_rou
user_router = Router()
default_router = Router()

@user_router.message(Command("start"))
async def cmd_start_user(message: types.Message, state: FSMContext):
    if await state.get_state() == States.user_state.state:
        await message.answer("You are already in user_state.")
    else:
        await state.set_state(States.user_state)
        await message.answer("State set to user_state.")

@user_router.message(Command("set_default"))
async def set_default_state(message: types.Message, state: FSMContext):
    await state.set_state(States.default)
    await message.answer("State changed to default.")
    await 

@default_router.message(Command("start"), States.default)
async def cmd_start_default(message: types.Message):
    await message.answer("You're in the default state.")

@default_router.message(Command("set_user_state"), States.default)
async def set_user_state(message: types.Message, state: FSMContext):
    await state.set_state(States.user_state)
    await message.answer("State changed to user_state.")

@user_router.message(Command("perms"))
async def grant_permission(message: types.Message , state : FSMContext):
    # await message.reply("testing1")

    user_chat_id = message.from_user.id
    tutorBool = db.child("users").child(user_chat_id).child("tutor").get()
    check_tutor = tutorBool.val()
    # await message.reply("testing")
    await message.reply(f"{str(user_chat_id)}, \n{str(check_tutor)}")

    if check_tutor == True:
        await state.set_state(tutor.mode)

        await message.reply("You have been granted permission to access more commands.")
    else:
        await message.reply("You do not have permission to use this command.")

@user_router.message(Command("restricted"), tutor.mode)
async def restricted_command(message: types.Message):
    await message.reply("You have access to this restricted command!")

@user_router.message(Command("check_subjects"), tutor.mode)
async def check_subjects(message: types.Message):
    # Query the database for all subjects
    subjects = db.child("Subject List").get()
    
    if subjects.each():
        # If there are subjects, format and send the list
        response = "Here are the existing subjects:\n\n"
        for subject in subjects.each():
            data = subject.val()
            response += f"Subject Name: {data['subject_name']}\nSubject Code: {data['subject_code']}\n\n"
    else:
        response = "No subjects found in the database."

    await message.answer(response)

# @user_router.message(state=Form.awaiting_command, commands=['more_commands'])
# async def more_commands(message: types.Message, state: FSMContext):
#     await message.reply("You have access to more commands!")

# @user_router.message(state='*', commands=['reset'])
# async def reset_state(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.reply("State has been reset. You no longer have special permissions.")



# @user_router.message(Command("testings"))
# async def cmd_start(message: types.Message):
#     await message.answer("Testing bot is working!", reply_markup= keyboard.testingKB)

# @user_router.callback_query(F.data == "tutor")
# async def tutor_callback(call: CallbackQuery, state : FSMContext):
#     await state.set(States.default)
#     await call.message.edit_text("Welcome, tutor. ", reply_markup= keyboard.tutorKB)
#     async def 
    


# /start command - create new subject for lecturers

@user_router.message(Command("create_subject"))
async def sub_input(call: CallbackQuery, state : FSMContext):
    await state.set_state(States.default)
    await call.message.edit_text("Enter the subject name:")
    await state.update_data(message=call)

# @user_router.message(States.default)
# async def sub_output(message: types.Message, state: FSMContext):
#     subject_name = message.text

#     # Query the database to check for duplicate subject names
#     existing_subjects = db.child("Subject List").order_by_child("subject_name").equal_to(subject_name).get()

#     if existing_subjects.each():
#         # If a duplicate is found, inform the user
#         await message.answer("This subject name already exists. Please enter a different subject name.")
#     else:
#         # Generate a random 6-digit subject code
#         def rand():
#             start = 10 ** (6 - 1)
#             end = (10 ** 6) - 1
#             return randint(start, end)

#         sub_code = (rand())

#         # Prepare the data to be added to the database
#         data = {
#             "subject_name": subject_name,
#             "subject_code": sub_code
#         }

#         # Add the new subject to the database
#         db.child("Subject List").child(sub_code).set(data)
#         await message.answer(f"Subject Name: {subject_name}\nSubject Code: ||{str(sub_code)}||", parse_mode="MarkdownV2")

#     # Clear the state
#     await state.clear()



    # stop command
@user_router.message(Command("stop"))
async def cmd_stop(message: types.Message):
    await message.answer("Bot stopping. Restart @ VS code.")
    asyncio.get_event_loop().call_later(0.5, sys.exit, 0)


 #respond to certain text in messages
@user_router.message()
async def echo_message(message: types.Message):
    if "hi" in message.text.upper() or "hello" in message.text.lower() or "hai " in message.text.lower():
        await message.answer("Hello brother! How are you?")
    elif "bye" in message.text.lower() or " bai " in message.text.lower()  or "cya" in message.text.lower():
        await message.answer("Bye brother! See you soon!")
        await cmd_stop(message)
    elif "nice" in message.text.lower():
        await message.answer("nice balls bro lol!")

#  uninterrupted service example : repeat message
@user_router.message(Command("repeat"))
async def repeat(message: types.Message, state: FSMContext):
    await message.answer("Tell me something and I will repeat it!")
    await message.answer("Enter your message:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(States.default)
    await state.update_data(message=message)

# applying the repeat state
@user_router.message(States.default)
async def process_input(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f"||{message.text}||", parse_mode="MarkdownV2")

#####








# admin infos 
@user_router.message(Command("admin_info"))
async def cmd_admin_info(message: types.Message, config: BotConfig):
    if message.from_user.id in config.admin_ids:
        await message.answer("You are an admin.")
    else:
        await message.answer("You are not an admin.")


#inline reply/callback 
@user_router.callback_query(F.data == "hello")
async def testingbro(query : CallbackQuery,config: BotConfig):
    await query.message.answer('LESGOOOOOOOOO')
    await cmd_start(query.message, config)

@user_router.callback_query(F.data== "hello1")
async def testingbro(query : CallbackQuery,config: BotConfig):
    await query.message.answer('This is the 2nd inline button lesgooooooo')
    await cmd_admin_info(query.message, config)




