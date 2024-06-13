from aiogram import Router, types , F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from bot.config import BotConfig
from bot import keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from random import randint
from ..firebase.fbauth import db, id_token
import sys, logging
import asyncio


# finite state class
# sets state to prevent interruption from other commands/responds
class student(StatesGroup):
    default = State()




# Set up logging, show message handling in real time
logging.basicConfig(level=logging.INFO)




user_router = Router()

@user_router.message(Command("start"))
async def startup(message: types.Message, state : FSMContext):
    userID = message.from_user.id
    username = message.from_user.username
    
    userdata = {
        "UserID" : userID,
        "Username" : username,
        "tutor" : False,
    }

    check_user = db.child("users").get(id_token)

    if check_user.each():

        tutorBool = db.child("users").child(userID).child("tutor").get(id_token)
        check_tutor = tutorBool.val()
        # await message.reply("testing")
        # await message.reply(f"{str(userID)}, \n{str(check_tutor)}")

        if check_tutor == True:
            await state.set_state(lecturer.default)
            logging.info("You are added as a lecturer.")
            await message.reply("Welcome back, lecturer.")
        elif check_tutor == False:
            await state.set_state(student.default)

            await message.reply("Welcome back, fellow student.")

    else: 
        db.child("users").child(userID).set(userdata, id)
        await state.set_state(student.default)
        await message.answer(f"Welcome to comm_Edubot, {str(username)}! ")




@user_router.message(Command("perms"),student.default)
async def grant_permission(message: types.Message , state : FSMContext):
    await message.reply("testing1")

  

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
#     await state.set(student.default)
#     await call.message.edit_text("Welcome, tutor. ", reply_markup= keyboard.tutorKB)
#     async def 
    


# /start command - create new subject for lecturers


    # Clear the state




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
    await state.set_state(student.default)
    await state.update_data(message=message)

# applying the repeat state
@user_router.message(student.default)
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
# @user_router.callback_query(F.data == "hello")
# async def testingbro(query : CallbackQuery,config: BotConfig):
#     await query.message.answer('LESGOOOOOOOOO')
#     # await cmd_start(query.message, config)

@user_router.callback_query(F.data== "hello1")
async def testingbro(query : CallbackQuery,config: BotConfig):
    await query.message.answer('This is the 2nd inline button lesgooooooo')
    await cmd_admin_info(query.message, config)




class lecturer(StatesGroup):
    default = State()
    creat_sub = State()
    check_students = State()


# testing if entered lect state
@user_router.message(Command("restricted"), lecturer.default)
async def restricted_command(message: types.Message):
    await message.reply("You have access to this restricted command!")

# check subject list of lecturer
@user_router.message(Command("check_subjects"), lecturer.default)
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

# @user_router.message(Command("pagination"))
# async def pagination(message: types.Message):
#     kb = types.InlineKeyboardMarkup()
#     paginator = Paginator(data=kb, size=5)
#     await message.answer(
#         text='Some menu',
#         reply_markup=paginator()
#     )


# page list thing


def get_subjects():
    try:
        logging.info("Attempting to fetch subjects from Firebase.")
        users_snapshot = db.child("Subject List").get(id_token)
        if users_snapshot.each() is None:
            logging.warning("No subjects found in Firebase.")
            return []
        users = [user.key() for user in users_snapshot.each()]
        logging.info(f"Retrieved subjects: {users}")
        return users
    except Exception as e:
        logging.error(f"Error fetching subjects: {e}")
        return []

current_page = 0
items_per_page = 5

def get_page(page_number, data):
    start = page_number * items_per_page
    end = start + items_per_page
    return data[start:end]

def create_navigation_buttons(page_number, total_pages):
    keyboard = InlineKeyboardMarkup()
    if page_number > 0:
        keyboard.insert(InlineKeyboardButton("⬅️ Previous", callback_data=f"prev_{page_number}"))
    if page_number < total_pages - 1:
        keyboard.insert(InlineKeyboardButton("Next ➡️", callback_data=f"next_{page_number}"))
    return keyboard

@user_router.message(Command("checklist"))
async def start_handler(message: types.Message, state: FSMContext):
    logging.info("Checklist command received.")
    subjects = get_subjects()
    if not subjects:
        await message.answer("No subjects found.")
        return
    
    total_pages = (len(subjects) + items_per_page - 1) // items_per_page
    page_data = get_page(current_page, subjects)
    list_text = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(page_data)])
    
    logging.info(f"Displaying page {current_page + 1} of {total_pages}")
    
    keyboard = create_navigation_buttons(current_page, total_pages)
    await message.answer(f"Page {current_page + 1}/{total_pages}\n{list_text}", reply_markup=keyboard)
    await state.set_state("pagination")

@user_router.callback_query(F.data.startswith("prev_"))
async def prev_page_handler(callback_query: types.CallbackQuery, state: FSMContext):
    global current_page
    logging.info(f"Previous page button clicked. Current page: {current_page}")
    current_page = int(callback_query.data.split("_")[1]) - 1
    subjects = get_subjects()
    total_pages = (len(subjects) + items_per_page - 1) // items_per_page
    page_data = get_page(current_page, subjects)
    list_text = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(page_data)])
    
    logging.info(f"Displaying page {current_page + 1} of {total_pages}")
    
    keyboard = create_navigation_buttons(current_page, total_pages)
    await callback_query.message.edit_text(f"Page {current_page + 1}/{total_pages}\n{list_text}", reply_markup=keyboard)

@user_router.callback_query(F.data.startswith("next_"))
async def next_page_handler(callback_query: types.CallbackQuery, state: FSMContext):
    global current_page
    logging.info(f"Next page button clicked. Current page: {current_page}")
    current_page = int(callback_query.data.split("_")[1]) + 1
    subjects = get_subjects()
    total_pages = (len(subjects) + items_per_page - 1) // items_per_page
    page_data = get_page(current_page, subjects)
    list_text = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(page_data)])
    
    logging.info(f"Displaying page {current_page + 1} of {total_pages}")
    
    keyboard = create_navigation_buttons(current_page, total_pages)
    await callback_query.message.edit_text(f"Page {current_page + 1}/{total_pages}\n{list_text}", reply_markup=keyboard)


@user_router.message(Command("create_subject"), lecturer.default)
async def sub_input(call: CallbackQuery, state : FSMContext):
    await state.set_state(lecturer.creat_sub)
    await call.message.edit_text("Enter the subject name:")
    await state.update_data(message=call)

@user_router.message(lecturer.creat_sub)
async def sub_output(message: types.Message, state: FSMContext):
    subject_name = message.text

    # Query the database to check for duplicate subject names
    existing_subjects = db.child("Subject List").order_by_child("subject_name").equal_to(subject_name).get()

    if existing_subjects.each():
        # If a duplicate is found, inform the user
        await message.answer("This subject name already exists. Please enter a different subject name.")
    else:
        # Generate a random 6-digit subject code
        def rand():
            start = 10 ** (6 - 1)
            end = (10 ** 6) - 1
            return randint(start, end)

        sub_code = (rand())

        # Prepare the data to be added to the database
        data = {
            "subject_name": subject_name,
            "subject_code": sub_code
        }

        # Add the new subject to the database
        db.child("Subject List").child(sub_code).set(data)
        await message.answer(f"Subject Name: {subject_name}\nSubject Code: ||{str(sub_code)}||", parse_mode="MarkdownV2")
        await state.set_state(lecturer.default)
