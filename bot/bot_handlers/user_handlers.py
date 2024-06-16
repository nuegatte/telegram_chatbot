from aiogram import Router, types , F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from bot.config import BotConfig
from bot import keyboard
# from bot.states import student, lecturer
from aiogram.fsm.context import FSMContext
from random import randint
from ..firebase.fbauth import db, id_token
import sys, logging
import asyncio
from aiogram.exceptions import TelegramNetworkError
from ..bot_handlers.paginator import items_per_page, get_page,extract_from_db,create_navigation_buttons, generate_list_text,calculate_total_pages
from aiogram.fsm.state import State, StatesGroup


class student(StatesGroup):
    default = State()

class lecturer(StatesGroup):
    default = State()
    create_sub = State()
    check_sub = State()
    check_students = State()



user_router = Router()
# finite state class
# sets state to prevent interruption from other commands/responds


# Set up logging, show message handling in real time
logging.basicConfig(level=logging.INFO)

@user_router.message(Command("start"))
async def startup(message: types.Message, state: FSMContext):
    userID = message.from_user.id
    username = message.from_user.username
    await handle_startup(userID, username, message, state)

async def handle_startup(userID: int, username: str, message: types.Message, state: FSMContext):

    
    userdata = {
        "UserID" : userID,
        "Username" : username,
        "tutor" : False,
    }

    check_user = db.child("users").get(id_token)

    if check_user.each():

        tutorBool = db.child("users").child(userID).child("tutor").get(id_token)
        check_tutor = tutorBool.val()

        if check_tutor == True:
            await state.set_state(lecturer.default)
            logging.info("You are added as a lecturer.")
            await message.answer("Welcome back, lecturer." , reply_markup= keyboard.tutor_kb)
        elif check_tutor == False:
            await state.set_state(student.default)

            await message.answer("Welcome back, fellow student.", reply_markup= keyboard.tutor_kb)

    else: 
        db.child("users").child(userID).set(userdata, id)
        await state.set_state(student.default)
        await message.answer(f"Welcome to comm_Edubot, {str(username)}! ")

@user_router.message(Command("getstate"))
async def get_state(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    logging.info(state_name)
    await message.answer(f"Current state: {state_name}")


@user_router.message(Command("admin_info"),lecturer.default)
async def cmd_admin_info(message: types.Message, config: BotConfig):
    logging.info("Admin info called.")
    if message.from_user.id in config.admin_ids:
        await message.answer(f"{message.from_user.id} You are an admin.")
    else:
        await message.answer(f"{message.from_user.id} You are not an admin.")

@user_router.message(Command("kbok"), lecturer.default)
async def okboss(message: types.Message, state : FSMContext):
    ok = await state.get_state()
    e = ok
    test = InlineKeyboardMarkup( inline_keyboard=[])
    test.inline_keyboard.append([InlineKeyboardButton(text = "test", callback_data= f"test{ok}")])
    logging.info(f"state is : {e}")
    await message.answer("hello",reply_markup= test)

@user_router.message(Command("about"), lecturer.default)
async def about_command(message: types.Message):
    await message.answer("This is a bot designed to assist lecturers in managing their subjects and students")


@user_router.message(Command("perms"),student.default)
async def grant_permission(message: types.Message ):
    await message.reply("testing1")

@user_router.message(Command("perms"),lecturer.default)
async def grant_permission(message: types.Message ):
    await message.reply("testing as lect")  

@user_router.message(Command("stop"))
async def cmd_stop(message: types.Message):
    await message.answer("Bot stopping. Restart @ VS code.")
    asyncio.get_event_loop().call_later(0.5, sys.exit, 0)


 #respond to certain text in messages
# @user_router.message()
# async def echo_message(message: types.Message):
#     if "hi" in message.text.upper() or "hello" in message.text.lower() or "hai " in message.text.lower():
#         await message.answer("Hello brother! How are you?")
#     elif "bye" in message.text.lower() or " bai " in message.text.lower()  or "cya" in message.text.lower():
#         await message.answer("Bye brother! See you soon!")
#         await cmd_stop(message)
#     elif "nice" in message.text.lower():
#         await message.answer("nice balls bro lol!")





@user_router.callback_query(F.data == "check_subject", lecturer.default)
async def cmd_checklist(call : types.CallbackQuery, state: FSMContext):
    await state.set_state(lecturer.check_sub)
    subjects = extract_from_db("Subject List")
    total_pages = calculate_total_pages(subjects)
    page_data = get_page(0, subjects)
    sub_list = generate_list_text(page_data)

    keyboard = create_navigation_buttons(0, total_pages, page_data)

    await call.message.edit_text(f"Page 1/{total_pages}\n\n{sub_list}", reply_markup=keyboard)



@user_router.callback_query(F.data.startswith("prev_") , lecturer.check_sub)
@user_router.callback_query(F.data.startswith("next_"), lecturer.check_sub)
async def subjectList_handler(call: types.CallbackQuery):
    global current_page
    direction, page_number = call.data.split("_")
    if direction == "prev":
        current_page = int(page_number) - 1
    elif direction == "next": 
        current_page = int(page_number) + 1
    
    subjects = extract_from_db("Subject List")
    total_pages = calculate_total_pages(subjects)
    page_data = get_page(current_page, subjects)
    sub_list = generate_list_text(page_data)

    keyboard = create_navigation_buttons(current_page, total_pages, page_data)
   
    try:
        await call.message.edit_text(f"Page {current_page + 1}/{total_pages}\n\n{sub_list}", reply_markup=keyboard)
    except TelegramNetworkError as e:
        logging.error(f"Network error when editing message: {e}")



@user_router.callback_query(F.data == "return", lecturer.check_sub)
async def return_to_menu(call : types.CallbackQuery, state : FSMContext):
    user_id = call.from_user.id
    username = call.from_user.username

    await handle_startup(user_id, username, call.message, state)



@user_router.callback_query(F.data == "create_sub", lecturer.default)
async def sub_input(call : CallbackQuery, state : FSMContext):

    await call.message.answer("Enter the subject name:")
    await state.set_state(lecturer.create_sub)
    s = await state.get_state()
    logging.info(f"State: {s}")   
    await state.update_data(message=call)

@user_router.message(lecturer.create_sub)
async def sub_output(message: types.Message, state: FSMContext):
    subject_name = message.text

    existing_subjects = db.child("Subject List").order_by_child("subject_name").equal_to(subject_name).get(id_token)

    if existing_subjects.each():
        await message.answer("This subject name already exists. Please enter a different subject name.")
    else:
        def rand():
            start = 10 ** (6 - 1)
            end = (10 ** 6) - 1
            return randint(start, end)

        sub_code = (rand())

        data = {
            "subject_name": subject_name,
            "subject_code": sub_code
        }

        db.child("Subject List").child(sub_code).set(data)
        await message.answer(f"Subject Name: {subject_name}\nSubject Code: ||{str(sub_code)}||", parse_mode="MarkdownV2")
        await state.set_state(lecturer.default)




@user_router.callback_query(F.data== "hello1", lecturer.default)
async def testingbro(call : CallbackQuery,config: BotConfig):
    await call.message.answer('Checking Admin info, callback = hello1')
    await cmd_admin_info(call.message, config)