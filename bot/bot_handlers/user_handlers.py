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
from aiogram.exceptions import TelegramNetworkError,TelegramBadRequest
from ..bot_handlers.paginator import   pagination, subject_access
from aiogram.fsm.state import State, StatesGroup


class student(StatesGroup):
    default = State()

class lecturer(StatesGroup):
    default = State()
    create_sub = State()
    check_sub = State()
    edit_sub = State()
    check_students = State()

class admin(StatesGroup):
    default = State()
    create_lecturer = State()
    check_lecturers = State()
    check_students = State()



user_router = Router()
# finite state class
# sets state to prevent interruption from other commands/responds


# Set up logging, show message handling in real time
logging.basicConfig(level=logging.INFO)


# startup handler
@user_router.message(Command("start"))
async def startup(message: types.Message, state: FSMContext, config : BotConfig):
    global userID
    userID = message.from_user.id
    username = message.from_user.username

    if userID in config.admin_ids:
        await state.set_state(admin.default)
        await message.answer("Welcome, admin!")

    else : 
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


@user_router.message(Command("about"), lecturer.default)
async def about_command(message: types.Message):
    await message.answer("This is a bot designed to assist lecturers in managing their subjects and students")




@user_router.message(Command("stop"))
async def cmd_stop(message: types.Message):
    await message.answer("Bot stopping. Restart @ VS code.")
    asyncio.get_event_loop().call_later(0.5, sys.exit, 0)




# Lecturer handlers

#    Subject Checker pagination
@user_router.callback_query(F.data == "check_subject", lecturer.default)
async def cmd_checklist(call : types.CallbackQuery, state: FSMContext):

    global subject_data
    subject_data =  db.child("Lecturers").child(userID).child("Subject_List").get(id_token)
    await state.set_state(lecturer.check_sub)
    first_page, kb = pagination(call,subject_data)

    await call.message.edit_text(first_page, reply_markup=kb)

#   prev, next page handling
@user_router.callback_query(F.data.startswith("prev_") , lecturer.check_sub)
@user_router.callback_query(F.data.startswith("next_"), lecturer.check_sub)
async def subjectList_handler(call: types.CallbackQuery):


    page, kb = pagination(call, subject_data)
   
    try:
        await call.message.edit_text(page, reply_markup=kb)
    except TelegramNetworkError as e:
        logging.error(f"Network error when editing message: {e}")

#   access, edit and delete subjects
@user_router.callback_query(F.data.startswith("item_"), lecturer.check_sub)
async def item_handler(call : types.CallbackQuery):


    subject_details, kb = subject_access(call, subject_data, userID)

    await call.message.edit_text(subject_details, reply_markup=kb)

#   return to subject checker
@user_router.callback_query(F.data == "back_toList", lecturer.check_sub)
async def back_to_list(call: types.CallbackQuery, state: FSMContext):

    await cmd_checklist(call, state)
        
#   return to menu 
@user_router.callback_query(F.data == "return", lecturer.default)
@user_router.callback_query(F.data == "return", lecturer.check_sub)
async def return_to_menu(call : types.CallbackQuery, state : FSMContext):
    user_id = call.from_user.id
    username = call.from_user.username

    await handle_startup(user_id, username, call.message, state)


    #  Subject Creation 
@user_router.callback_query(F.data == "create_sub", lecturer.default)
async def sub_input(call : CallbackQuery, state : FSMContext):

    await call.message.answer("Enter the subject name:")
    await state.set_state(lecturer.create_sub)
    s = await state.get_state()
    logging.info(f"State: {s}")   
    await state.update_data(message=call)

@user_router.message(lecturer.create_sub)
async def sub_output(message: types.Message, state: FSMContext):
    async def retry(error_message :str):
        await state.set_state(lecturer.default)
        retry_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Retry", callback_data="create_sub")]
            ]
        )
        await message.answer(error_message, reply_markup= retry_button)

    try:
        id = message.from_user.id
        subject_name = message.text

        # existing_subjects = db.child("Lecturers").child(id).order_by_child("Subject_List").equal_to(subject_name).get(id_token)
        subjects_ref = db.child("Lecturers").child(id).child("Subject_List")
        existing_subjects = subjects_ref.order_by_child("subject_name").equal_to(subject_name).get(id_token)


        if existing_subjects.each():
            retry("This subject name already exists. Please enter a different subject name.")
        else:
            def rand():
                start = 10 ** (6 - 1)
                end = (10 ** 6) - 1
                return randint(start, end)

            sub_code = (rand())

            data = {
                "subject_name": subject_name,
                "subject_code": sub_code,
                "student_list": {}
            }
            await state.set_state(lecturer.default)
            db.child("Lecturers").child(id).child("Subject_List").child(subject_name).set(data, id_token)
            await message.answer(f"Subject Name: {subject_name}\nSubject Code: ||{str(sub_code)}||", parse_mode="MarkdownV2", reply_markup= keyboard.return_button)
    except TelegramBadRequest as e:
        await retry("Other symbols (!, @, #, $, etc.) are not allowed in a subject name, please try again.")
    except Exception as e:
        await retry("An error occurred while processing your request. Please try again later.")


@user_router.callback_query(F.data.startswith("delete_"), lecturer.check_sub)
async def delete_subject(call: types.CallbackQuery, state: FSMContext):
    subject = call.data.split("_")[1]
    db.child("Subject List").child(subject).remove(id_token)
    await call.answer(f"Subject {subject} deleted.")
    await back_to_list(call, state)

@user_router.callback_query(F.data.startswith("edit_"), lecturer.check_sub)
async def edit_subject_name(call: types.CallbackQuery, state: FSMContext):
    subject = call.data.split("_")[1]
    await state.update_data(subject_to_edit=subject)
    await call.message.edit_text(f"Enter new name for subject {subject}:")
    await state.set_state(lecturer.edit_sub)


@user_router.message(F.text, lecturer.edit_sub) 
async def enter_new_subject_name(message: types.Message, state: FSMContext):
    new_name = message.text
    data = await state.get_data()
    subject = data.get("subject_to_edit")
    subject_data = db.child("Subject List").child(subject).get(id_token).val()

    # Update the subject with the new name
    db.child("Subject List").child(subject).remove(id_token)
    db.child("Subject List").child(new_name).set(subject_data, id_token)
    await state.set_state(lecturer.check_sub)
    await message.answer(f"Subject name changed to {new_name}.", reply_markup= keyboard.return_button)



#  Testings
@user_router.callback_query(F.data== "hello1", lecturer.default)
async def testingbro(call : CallbackQuery,config: BotConfig):
    await call.message.answer('Checking Admin info, callback = hello1')
    await cmd_admin_info(call.message, config)

@user_router.message(Command("perms"),student.default)
async def grant_permission(message: types.Message ):
    await message.reply("testing1")

@user_router.message(Command("perms"),lecturer.default)
async def grant_permission(message: types.Message ):
    await message.reply("testing as lect")  

