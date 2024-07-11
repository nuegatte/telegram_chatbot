from aiogram import Router, types , F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, Filter
from aiogram.filters.callback_data import CallbackData
from bot.config import BotConfig
from bot import keyboard
# from bot.states import student, lecturer
from aiogram.fsm.context import FSMContext
from random import randint
from ..firebase.fbauth import db, id_token
import sys, logging
import asyncio
from aiogram.exceptions import TelegramNetworkError,TelegramBadRequest
from ..bot_handlers.paginator import   pagination, extract_from_db
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods.send_message import SendMessage
from bot_instance import bot

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
    get_user_locale
from datetime import datetime
from aiogram.enums import ChatType

# finite state class
# sets state to prevent interruption from other commands/responds
class registration(StatesGroup):
    default = State()
    enter_name = State()
    join_subject = State()

class Student(StatesGroup):
    default = State()
    join_subject = State()

class Lecturer(StatesGroup):
    default = State()
    create_class = State()
    check_class = State()
    edit_sub = State()
    check_students = State()

    create_ann = State()
    ann_title = State()
    ann_content = State()

    create_sub_ann = State()
    sub_ann_title = State()
    sub_ann_content = State()

class Admin(StatesGroup):
    default = State()
    create_lecturer = State()
    check_lecturers = State()
    check_users = State()


user_router = Router()

# Define filters
class PrivateChatFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type == ChatType.PRIVATE


# Attach filters to routers
user_router.message.filter(PrivateChatFilter())


# from meeting jul 5th
# schedule notif
# publish assignment 
# make assignment date
# alicloud for hosting 
#subject_FAQ 
# Set up logging, show message handling in real time

# see if possible , creat group chat and then make threads that canbe used for discussions 
#  some of the other functiosn can update within private chat 
#  but some of the other functions can be done in group chat

# chnge to make it usable for any type of classroom
# since most people these days know how to text on whatsapp
#  they are most familiar with chatting system like chatgpt and whatsapp 
# the bot is make so that they can get used to a system like this in the system they have already been most familiarised with 
# get everything done by todya midnight and explode 
# chap 1 2 3 report


logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

#                 _      _
#                | |    | |
#   _ __   _   _ | |__  | |(_)  ___ 
#  | '_ \ | | | || '_ \ | || | / __|
#  | |_) || |_| || |_) || || || (__ 
#  | .__/  \__,_||_.__/ |_||_| \___|
#  |_|            

# startup handler
@user_router.message(Command("start"))
async def startup(message: types.Message, state: FSMContext, config : BotConfig):
    # globalised user details for 
    global user_id

    user_id = message.from_user.id


    # await message.reply(f"name : {username}\n user_id: {user_id}")
    if user_id in config.admin_ids:
        await state.set_state(Admin.default)
        await message.answer("Welcome, admin!", reply_markup=keyboard.admin_kb)

    else : 

        await handle_startup(user_id,  message, state)




async def handle_startup(user_id: int, message: types.Message, state: FSMContext):
    # check_user = db.child("users").get(id_token)
    logging.info("this is the user point.")

    try:
        # user_id = message.from_user.id
        check_user = db.child("users").child(user_id).get(id_token)
        if check_user.val() is not None:
            tutorBool = db.child("users").child(user_id).child("tutor").get(id_token)
            check_tutor = tutorBool.val()
            logging.info(f"is tutor : {check_tutor}")
            if check_tutor is True:
                await state.set_state(Lecturer.default)
                logging.info("You are added as a Lecturer.")
                await message.answer("Welcome back, Lecturer.", reply_markup=keyboard.lect_kb)
                logging.info("shuld be replying now ")

                # simulated_callback_query = types.CallbackQuery(
                #     id='1',
                #     from_user=message.from_user,
                #     data="check_subject",
                #     message=message,
                #     chat_instance='simulated_chat_instance'  # Add the required field
                # )

                # await cmd_checklist(simulated_callback_query, state)
            elif check_tutor is False:
                logging.info("You are added as a Student.")
                await state.set_state(Student.default)

                await message.answer("Welcome back, fellow Student.", reply_markup=keyboard.student_kb)
        else:

            await message.answer("I sense a new user...please proceed to register", reply_markup=keyboard.register_button)
            await state.set_state(registration.default)
            # db.child("users").child().set(userdata, id_token)
            # await message.answer(f"Welcome to comm_Edubot, {str(user_id)}!")
    except Exception as e:
        logging.error(f"Error in handle_startup: {e}")
        await message.answer("An error occurred. Please try again later.")




@user_router.callback_query(F.data == "return", Admin.check_users)
async def admin_startup(call : CallbackQuery, state : FSMContext):
    await state.set_state(Admin.default)
    await call.message.edit_text("Welcome, admin!", reply_markup=keyboard.admin_kb)




# registration process
@user_router.callback_query(F.data =="registry", registration.default)
async def registry(call : CallbackQuery, state : FSMContext):
    await call.message.edit_text("Please enter your preferred username.\n\nYour real name is recommended so that\nyour lecturer can identify you clearly.")
    await state.set_state(registration.enter_name)




@user_router.message(registration.enter_name)
async def regis_handler(message : types.Message, state : FSMContext):
    async def retry(error_message :str):
        await state.set_state(registration.default)
        retry_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Retry", callback_data="registry")]
            ]
        )
        await message.answer(error_message, reply_markup= retry_button)

    global entered_name
    entered_name = message.text

    try:
        users = db.child("users").get(id_token)
        if users.each():
            for user in users.each():
                if user.val().get("Username") == entered_name:
                    await retry(f"Username already exists, please add any symbol, or numbers like {str(entered_name)}123")
                    return

        await message.answer(f"Proceed with the following name?\n\n<b>{str(entered_name)}</b>", parse_mode="HTML", reply_markup=keyboard.registry)
        await state.update_data(entered_name=entered_name)
    except Exception as e:
        await retry("Unexpected error occurred, try again.")





@user_router.callback_query(F.data =="confirm_registration", registration.enter_name)
async def regis_success(call:CallbackQuery, state : FSMContext ):
    user_data = {
        user_id: {
            "username" : entered_name,
            "user_id" : user_id,
            "tutor" : False
        }

    }

    student_data = {
        user_id: {
            "username" : entered_name,
            "user_id" : user_id,

        }
    }
    db.child("users").update(user_data, id_token)
    db.child("Students").update(student_data, id_token)
    await call.message.edit_text(f"Welcome to comm_Edubot, {str(entered_name)}")

    await handle_startup(user_id,call.message, state)



#      _        _             _          _   _                    _  _                  
#     / \    __| | _ __ ___  (_) _ __   | | | |  __ _  _ __    __| || |  ___  _ __  ___ 
#    / _ \  / _` || '_ ` _ \ | || '_ \  | |_| | / _` || '_ \  / _` || | / _ \| '__|/ __|
#   / ___ \| (_| || | | | | || || | | | |  _  || (_| || | | || (_| || ||  __/| |   \__ \
#  /_/   \_\\__,_||_| |_| |_||_||_| |_| |_| |_| \__,_||_| |_| \__,_||_| \___||_|   |___/
                                                                                      
#   admin handlers Must not be visible to the public at all
#   only include admin handlers with admin context and reply keyboard markup. and callbacks.

@user_router.message(Command("cal"))
async def nav_cal_handler(message: types.Message):
    await message.answer(
        "Please select a date: ",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
    )

@user_router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.edit_text(
            f'You selected {date.strftime("%d/%m/%Y")}\n'
            f'selected var --> {str(selected)}\n'
            f'date --> {str(date)}'
        )

@user_router.message(Command("notify"), Admin.default)
async def notify(message: types.Message, state: FSMContext):
    try:
        users = db.child("users").get(id_token)
        if users.each():
            for user in users.each():
                getuser= user.key()
                try:
                    await bot.send_message(chat_id=getuser, text="This is a notification message.")
                except Exception as e:
                    await message.answer(f"Failed to send message to {user_id}: {e}")
        else:
            await message.answer("No users found in the database.")
    except Exception as e:
        await message.answer(f"Your error is : \n {e}")


@user_router.callback_query(F.data == "admin_cmd_list", Admin.default)
async def cmd_list_admin(call: types.CallbackQuery):

    await call.answer("Your command lists are")





@user_router.callback_query(F.data == "check_lect", Admin.default)
async def cmd_check_lect(call: types.CallbackQuery):
    global lect_data
    lect_data = db.child("Lecturers").get(id_token)

    logging.info(f"{lect_data}")
    ok = extract_from_db(lect_data)
    logging.info(f"{ok}")
    first_page, kb = pagination(call, lect_data)
    await call.message.edit_text(first_page, reply_markup=kb)



#   check users
@user_router.callback_query(F.data == "check_users", Admin.default)
async def cmd_check_users(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Admin.check_users)
    logging.info("Fetching user list.")

    global users
    users = db.child("users").get(id_token).val()
    
    # user_list = {user.key(): user.val()['username'] for user in users.each()}
    # logging.info(user_list)
    global user_extractor
    def user_extractor(user_item):
        user_id, user_info = user_item
        return (user_id, user_info['username'])
    
    ok = extract_from_db(users, user_extractor)
    logging.info(ok)
    first_page, kb = pagination(call, users,user_extractor)
    await call.message.edit_text(first_page, reply_markup=kb)




@user_router.callback_query(F.data.startswith("prev_"), Admin.check_users)
@user_router.callback_query(F.data.startswith("next_"), Admin.check_users)
async def user_list_handler(call: types.CallbackQuery, state: FSMContext):

    page, kb = pagination(call,users,  user_extractor )
    try:
        await call.message.edit_text(page, reply_markup=kb)
    except TelegramNetworkError as e:
        logging.error(f"Network error when editing message: {e}")





@user_router.callback_query(F.data.startswith("item_"), Admin.check_users)
async def user_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_list = data.get("user_list")
    index = int(call.data.split("_")[1])
    
    user_keys = list(user_list.keys())
    if index < len(user_keys):
        user_id = user_keys[index]
        user = db.child("users").child(user_id).get(id_token).val()
        
        user_details = (f"Username: {user['username']}\n"
                        f"UserID: {user['user_id']}\n"
                        f"Tutor: {user['tutor']}")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Back", callback_data="back_toList")],
            [InlineKeyboardButton(text="Return to menu", callback_data="return")]
        ])
        
        await call.message.edit_text(user_details, reply_markup=keyboard)





@user_router.callback_query(F.data == "back_toList", Admin.check_users)
async def back_to_list(call: types.CallbackQuery, state: FSMContext):
    await cmd_check_users(call, state)




@user_router.callback_query(F.data == "admin_check_stud", Admin.default)
@user_router.callback_query(F.data == "edit_class", Admin.default)
@user_router.callback_query(F.data == "log_off", Admin.default)


#   ____   _               _               _     _   _                    _  _                  
#  / ___| | |_  _   _   __| |  ___  _ __  | |_  | | | |  __ _  _ __    __| || |  ___  _ __  ___ 
#  \___ \ | __|| | | | / _` | / _ \| '_ \ | __| | |_| | / _` || '_ \  / _` || | / _ \| '__|/ __|
#   ___) || |_ | |_| || (_| ||  __/| | | || |_  |  _  || (_| || | | || (_| || ||  __/| |   \__ \
#  |____/  \__| \__,_| \__,_| \___||_| |_| \__| |_| |_| \__,_||_| |_| \__,_||_| \___||_|   |___/
                                                                                              
# student handlers

#   Joining a classroom
@user_router.callback_query(F.data == "join_subject", Student.default)
async def join_prompt(call: CallbackQuery, state: FSMContext):
    await state.set_state(Student.join_subject)
    prompt = ("Enter your Enrolment code!\n\n"
              "Your lecturer should have given you a 6-digit code\n"
              "in class and sending here right now will allow\n"
              "you to join a class.")
    await call.message.edit_text(prompt)
    await state.update_data(message=call)

@user_router.message(Student.join_subject)
async def join_sub(message: types.Message, state: FSMContext):
    try:
        retry = keyboard.retry_button("join_subject")
        input_code = message.text

        # Convert input_code to integer

        # Log the query URL for debugging
        logging.info(f"Querying for Enrolment code: {input_code}")

        # Querying the database
        db_subject_code = db.child("Class_List").order_by_child("enrol_code").equal_to(int(input_code)).get(id_token)

        # Log the result of the query
        logging.info(f"Query result: {db_subject_code.val()}")

        global username 
        username = db.child("users").child(user_id).get(id_token).val().get('username')
        stud_detail = {
            user_id: {
                "User_ID": user_id,
                "Student Name": username
            }
        }

        # Check if lect has setup the group yet
        check_if_setup = db.child("Class_List").child(input_code).get(id_token).val().get('chat_id')
        if check_if_setup is None:
            reminder = (
                "This Enrolment code is not setup in a group chat yet.\n"
                "Please contact your teacher to setup this Enrolment code.\n\n"
                "If you are with your teacher, please use the /setup command to \n"
                "setup this Enrolment code in a groupchat.\n"
                "Make sure that the groupchat is a <b>supergroup<b>!"
            )
            await message.answer(reminder, reply_markup=retry)
        
        elif check_if_setup is not None:
            if db_subject_code.each():
                sub_user_list = db.child("Class_List").child(input_code).child("student_list")

                check_user = sub_user_list.order_by_child("User_ID").equal_to(user_id).get(id_token)
                chat_id = check_if_setup

                invite_link = await bot.export_chat_invite_link(chat_id)


                class_lect = db.child("Class_List").child(input_code).child("lecturer_id").get(id_token).val()
                class_name = db.child("Class_List").child(input_code).child("class_name").get(id_token).val()
                class_code = db.child("Class_List").child(input_code).child("enrol_code").get(id_token).val()

                student_class_data = {
                    class_code: {
                        "lect_id" : class_lect,
                        "class_name": class_name,
                        "enrol_code": class_code,
                        "chat_id": chat_id,
                    }

                }

                try:
                    if check_user.each():
                        await state.set_state(Student.default)
                        await message.answer("You are already in this class!, here is the invite link if you havent joined yet..", reply_markup=retry)
                        await message.answer(invite_link)
                    else:
                        lect_id = db.child("Class_List").child(int(input_code)).get(id_token).val().get('lecturer_id')
                        db.child("Lecturers").child(lect_id).child("student_list").update(stud_detail,id_token)
                        db.child("Class_List").child(input_code).child("student_list").update(stud_detail, id_token)
                        db.child("Students").child(user_id).child("Class_List").update(student_class_data,id_token)
                        await state.set_state(Student.default)
                        await message.answer("You have successfully joined the class!", reply_markup=keyboard.return_button)
                        await message.answer(invite_link)
                except TelegramBadRequest as e:
                    logging.info(f"Telegram error: {e}")
                    await message.answer(f"This is from check side, \n\n{e}")
                except Exception as e:
                    await message.answer(f"{e}\n\nYou got error, retry.", reply_markup=retry)
            else:
                await state.set_state(Student.default)
                await message.answer(f"error : {e} \n\ninput code : {str(input_code)}\nmatching : {db_subject_code.val()}\nEnrolment code not found, please try again.", reply_markup=retry)
    except AttributeError as e:
        logging.info(f"Telegram error: {e}")
        err = (
            f"The class enrolment code does exist, but....\n"
            f"your teacher has not set it up properly in a \n"
            f"super group. \n\n"
            "Please contact your teacher to fix this issue"
        )
        await message.answer(err, reply_markup= retry)
    
    except TelegramBadRequest as e:
        logging.info(f"Telegram error: {e}")
        await message.answer(f"This is from first layer check, \n\n{e}")  
    except UnboundLocalError as e:
        await state.set_state(Student.default)
        await message.answer(f"The Enrolment code you have entered ({input_code}) is not found.\n\nPlease re-enter the correct/other enrolment codes.", reply_markup=retry)
    except Exception as e:
        await state.set_state(Student.default)

        err = f"Your entered input: {input_code}\nExisting clss? {db_subject_code}\nError: {e}"
        logging.info(err)
        await message.answer(err, reply_markup=retry)

        



# do not enter any student related handlers beyond this point 




#   _                 _                             _   _                    _  _                  
#  | |     ___   ___ | |_  _   _  _ __  ___  _ __  | | | |  __ _  _ __    __| || |  ___  _ __  ___ 
#  | |    / _ \ / __|| __|| | | || '__|/ _ \| '__| | |_| | / _` || '_ \  / _` || | / _ \| '__|/ __|
#  | |___|  __/| (__ | |_ | |_| || |  |  __/| |    |  _  || (_| || | | || (_| || ||  __/| |   \__ \
#  |_____|\___| \___| \__| \__,_||_|   \___||_|    |_| |_| \__,_||_| |_| \__,_||_| \___||_|   |___/1
                                                                                                 

#    classroom Checker pagination
@user_router.callback_query(F.data == "check_subject", Lecturer.default)
@user_router.callback_query(F.data == "select_subject", Lecturer.create_ann)
async def cmd_checklist(call : types.CallbackQuery, state: FSMContext):

    curr_state = await state.get_state()
    if curr_state == Lecturer.default:
        await state.set_state(Lecturer.check_class)
    elif curr_state == Lecturer.create_ann:
        pass
    
    global classroom_data
    classroom_data =  db.child("Lecturers").child(user_id).child("Class_List").get(id_token)
    logging.info(f"{classroom_data}")
    # await state.set_state(Lecturer.check_class)

    global classroom_extractor 
    def classroom_extractor (class_data):
        return class_data.key()
    
    first_page, kb = pagination(call,classroom_data, classroom_extractor )

    await call.message.edit_text(first_page, reply_markup=kb)




#   prev, next page handling
@user_router.callback_query(F.data.startswith("prev_") , Lecturer.check_class)
@user_router.callback_query(F.data.startswith("prev_") , Lecturer.create_ann)
@user_router.callback_query(F.data.startswith("next_"), Lecturer.check_class)
@user_router.callback_query(F.data.startswith("next_"), Lecturer.create_ann)
async def subjectList_handler(call: types.CallbackQuery):
    page, kb = pagination(call, classroom_data, classroom_extractor )
   
    try:
        await call.message.edit_text(page, reply_markup=kb)
    except TelegramNetworkError as e:
        logging.error(f"Network error when editing message: {e}")



#   access, edit and delete subjects
@user_router.callback_query(F.data.startswith("item_"), Lecturer.check_class)
async def item_handler(call : types.CallbackQuery):
    index = int(call.data.split("_")[1])
    objects = extract_from_db(classroom_data, classroom_extractor )
    global class_data, clss, st_list

    clss = objects[index]
    class_data = db.child("Lecturers").child(user_id).child("Class_List").child(clss).get(id_token).val()
    st_list = db.child("Class_List").child((class_data.get("enrol_code"))).child("student_list").get(id_token).val()
    std_count = len(st_list) - 1

    if index < len(objects):
  
        subject_details = (
            f"Class name : {clss}\n"
            f"Enrolment code : {class_data.get('enrol_code')}\n"
            f"Student count : {std_count}"
        )
        subject_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Back", callback_data="back_toList")],
            [InlineKeyboardButton(text="Delete classroom", callback_data=f"delete_{clss}")],
            [InlineKeyboardButton(text="Edit Class name", callback_data=f"edit_{clss}")],
            [InlineKeyboardButton(text="Return to menu", callback_data="return")]
        ])

    # subject_details, kb = subject_access(call, classroom_data, user_id, classroom_extractor )

    await call.message.edit_text(subject_details, reply_markup=subject_keyboard)


@user_router.callback_query(F.data.startswith("delete_"), Lecturer.check_class)
async def delete_subject(call: types.CallbackQuery, state: FSMContext):
    classroom = call.data.split("_")[1]
    matching_code = class_data.get('enrol_code')
    db.child("Lecturers").child(user_id).child("Class_List").child(classroom).remove(id_token)
    db.child("Class_List").child(matching_code).remove(id_token)
    await call.answer(f"classroom {classroom} deleted.")
    await back_to_list(call, state)




@user_router.callback_query(F.data.startswith("edit_"), Lecturer.check_class)
async def edit_subject_name(call: types.CallbackQuery, state: FSMContext):
    classroom = call.data.split("_")[1]
    await state.update_data(subject_to_edit=classroom)
    await call.message.edit_text(f"Enter new name for classroom {classroom}:")
    await state.set_state(Lecturer.edit_sub)




@user_router.message(F.text, Lecturer.edit_sub) 
async def enter_new_subject_name(message: types.Message, state: FSMContext):
    new_name = message.text
    data = await state.get_data()
    classroom = data.get("subject_to_edit")
    matching_code = class_data.get('enrol_code')

    lect_subject_data = db.child("Lecturers").child(user_id).child("Class_List").child(classroom).get(id_token).val()
    lect_subject_data["class_name"] = new_name
    sublist_data = db.child("Class_List").child(int(matching_code)).get(id_token).val()
    sublist_data["class_name"] = new_name

    db.child("Lecturers").child(user_id).child("Class_List").child(classroom).remove(id_token)
    db.child("Lecturers").child(user_id).child("Class_List").child(new_name).set(lect_subject_data, id_token)
    # db.child("Class_List").child(matching_code).remove(id_token)
    db.child("Class_List").child(matching_code).set(sublist_data,id_token)
    
    await state.set_state(Lecturer.check_class)
    await message.answer(f"Class name changed to {new_name}.", reply_markup= keyboard.return_button)




#   return to classroom checker
@user_router.callback_query(F.data == "back_toList", Lecturer.check_class)
async def back_to_list(call: types.CallbackQuery, state: FSMContext):

    await cmd_checklist(call, state)
        


# making announcements 
@user_router.callback_query(F.data == "create_announcement", Lecturer.default)
async def create_announcement(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Lecturer.create_ann)
    await call.message.edit_text("Select your announcement type", reply_markup= keyboard.lect_ann_kb)


#   general announcements

#   classroom specific announecement, F.check_suhject, then this. 
@user_router.callback_query(F.data.startswith("item_"), Lecturer.create_sub_ann)
async def item_handler(call : types.CallbackQuery, state : FSMContext):
    index = int(call.data.split("_")[1])
    objects = extract_from_db(classroom_data, classroom_extractor )
    global ann_subdata, ann_sub, ann_st_list

    ann_sub = objects[index]
    ann_subdata = db.child("Lecturers").child(user_id).child("Class_List").child(ann_sub).get(id_token).val()
    ann_st_list = db.child("Class_List").child((ann_subdata.get("enrol_code"))).child("student_list").get(id_token).val()


    if index < len(objects):
        subject_details = (
            f"Class name : {ann_sub}\n"
            f"Enrolment code : {ann_subdata.get('enrol_code')}\n\n"
            f"Please enter the <b>title</b> of your announcement.\n"
            f"Example : Assignment 1 due date, Class replacement announcement."
        )


    # subject_details, kb = subject_access(call, classroom_data, user_id, classroom_extractor )

    await call.message.edit_text(subject_details,parse_mode="HTML")
    await state.set_state(Lecturer.ann_title)
    await state.update_data(message=call)


@user_router.message(Lecturer.sub_ann_title)
async def ann_title(message: types.Message, state: FSMContext):
    global title
    title =await state.get_data()

    msg = (
        f"Your announcement title : {title}"
        f"\n\nPlease enter your announcement <b>content</b>."
        f"\n\nExample : The assignment is due on 20th of May."
    )
    await message.answer(msg, parse_mode="HTML")
    await state.set_state(Lecturer.ann_content)
    await state.update_data(message=message)








#   return to menu 
@user_router.callback_query(F.data == "return", Lecturer.default)
@user_router.callback_query(F.data == "return", Lecturer.check_class)
@user_router.callback_query(F.data == "return", Lecturer.create_class)
@user_router.callback_query(F.data == "return", Student.join_subject)
@user_router.callback_query(F.data == "return", Student.default)
async def return_to_menu(call : CallbackQuery, state : FSMContext):
    await call.message.edit_text("Returning to menu.")
    await handle_startup(user_id,call.message,state)



    #  classroom Creation 
@user_router.callback_query(F.data == "create_sub", Lecturer.default)
async def sub_input(call : CallbackQuery, state : FSMContext):

    await call.message.edit_text("Enter the Class name:")
    await state.set_state(Lecturer.create_class)
    s = await state.get_state()
    logging.info(f"State: {s}")   
    await state.update_data(message=call)

#   classroom creation
@user_router.message(Lecturer.create_class)
async def sub_output(message: types.Message, state: FSMContext):


    try:

        class_name = message.text
        retry = keyboard.retry_button("create_sub") 

        # existing_subjects = db.child("Lecturers").child(id).order_by_child("Class_List").equal_to(class_name).get(id_token)
        subjects_ref = db.child("Lecturers").child(user_id).child("Class_List")
        existing_subjects = subjects_ref.order_by_child("class_name").equal_to(class_name).get(id_token)
        logging.info(existing_subjects.val())
#       lecturer themselves cannot have duplicate Class name
#       classroom names however can be duplicate, as it is mainly identified by the Enrolment code itself 
        if existing_subjects.each():
            # retry("This Class name already exists. Please enter a different Class name.", Lecturer.default, "create_class")
            await state.set_state(Lecturer.default)
            await message.answer("This Class name already exists.\nPlease enter a different Class name.", reply_markup = retry)

            
        else:
            def rand():
                start = 10 ** (6 - 1)
                end = (10 ** 6) - 1
                return randint(start, end)

            enrol_code = (rand())

            class_data = {
                enrol_code: {
                    "lecturer_id" : user_id,
                    "class_name": class_name,
                    "enrol_code": enrol_code,
                    "student_list": {
                        "placehodler":"placeholder"
                    }
                }
            }
#                   student list schema { user_id : user_name}

            lect_class_data = {
                "class_name": class_name,
                "enrol_code": enrol_code,

            }

            await state.set_state(Lecturer.default)
            db.child("Class_List").update(class_data,id_token)

            db.child("Lecturers").child(user_id).child("Class_List").child(class_name).set(lect_class_data, id_token)


            success_message = (
                f"Class name: {class_name}\n"
                f"Enrol Code: ||{str(enrol_code)}||\n\n"
                "What do I do now? \n\n"
                "1\\. Create a group chat, and turn it into a Super group\\.\n\n"
                "2\\. Add me into the group chat, and use /setup command\\.\n\n"
                "3\\. I will set up the classroom and an invite link to join the class\\.\n\n"
                f"4\\. Share the enrolment code \\({str(enrol_code)}\\) with your students\n"
                "    so they can get the invite link for the group chat from me\\!\n\n"
                "5\\. Forward the code below once you finished /setup in the group chat\\!\\!\n\n\n"
                "Happy teaching\\!"
            )

            await message.answer(success_message, parse_mode="MarkdownV2", reply_markup= keyboard.return_button)
            await message.answer(str(enrol_code))
    except TelegramBadRequest as e:
        await state.set_state(Lecturer.default)
        await message.answer(f"error : {e}\n\nOther symbols (!, @, #, $, etc.) are not allowed in a Class name, please try again.", reply_markup = retry)
    except Exception as e:
        await state.set_state(Lecturer.default)
        await message.answer(f"error : {e}\n\nAn error occurred while processing your request. Please try again later.", reply_markup = retry)
    


# Info Checking for Lecturer mode.
#  Testings


# @user_router.message(Command("perms"),Student.default)
# @user_router.message(Command("perms"),Lecturer.default)
@user_router.message(Command("perms"))
async def check_perms(message: types.Message, state : FSMContext):
    curr_state = await state.get_state()

    try: 
        if curr_state == F.data.startswith(Admin):

            await message.answer(f"State : {str(curr_state)}\nPermissions : Admin") 


        elif curr_state == F.data.startswith(Student):

            await message.answer(f"State : {str(curr_state)}\nPermissions : Student") 


        elif curr_state == F.data.startswith(Lecturer):

            await message.answer(f"State : {str(curr_state)}\nPermissions : Lecturer")
        else:
            await message.answer(f"State : {str(curr_state)}\nPermissions : others ")


    except Exception as e:

        await message.answer("Error occured. Rejoining session.")
        await handle_startup(user_id, message, state)






                                                

# ████████ ███████ ███████ ████████ ██ ███    ██  ██████  
#    ██    ██      ██         ██    ██ ████   ██ ██       
#    ██    █████   ███████    ██    ██ ██ ██  ██ ██   ███ 
#    ██    ██           ██    ██    ██ ██  ██ ██ ██    ██ 
#    ██    ███████ ███████    ██    ██ ██   ████  ██████  
                                                        
                                                        

                                                        
                                                    
@user_router.message(Command("perms"),Lecturer.default)
async def grant_permission(message: types.Message ):
    await message.reply("testing as lect")  




@user_router.message(Command("admin_info"),Student.default)
@user_router.message(Command("admin_info"),Lecturer.default)
@user_router.message(Command("admin_info"),Admin.default)
async def cmd_admin_info(message: types.Message, config: BotConfig):
    logging.info("Admin info called.")
    if message.from_user.id in config.admin_ids:
        await message.answer(f"{message.from_user.id} You are an Admin.")
    else:
        await message.answer(f"{message.from_user.id} You are not an Admin.")




@user_router.message(Command("about"), Admin.default)
@user_router.message(Command("about"), Student.default)
@user_router.message(Command("about"), Lecturer.default)
async def about_command(message: types.Message, state : FSMContext):
    curr_state = await state.get_state()

#   add inline baord to return to their respective main menu after showing the about messages 
    try: 
        if curr_state == Admin.default:

            await message.answer("You are an Admin.") 


        elif curr_state == Student.default:

            await message.answer("You are a Student.")

        elif curr_state == Lecturer.default:

            await message.answer("You are a Lecturer.")

    except Exception as e:

        await message.answer("Error occured. Rejoining session.")
        user_id = message.from_user.id
        await handle_startup(user_id, message, state)




@user_router.message(Command("testingwater"))
async def testingwater(message: types.Message):
    ok = {
        "result": {
            "id": 1,
            "first_name": "John",
            "last_name": "Smith",
            "username": "JohnSmith",
            "language_code": "en"
        }
    }

    db.child("Testing Strucutre").update(ok, id_token)
    await message.answer("Testing Water Done ")

    # testing commands 




@user_router.message(Command("getstate"))
async def get_state(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    logging.info(state_name)
    await message.answer(f"Current state: {state_name}")




@user_router.message(Command("stop"))
async def cmd_stop(message: types.Message):
    await message.answer("Bot stopping. Restart @ VS code.")
    asyncio.get_event_loop().call_later(0.5, sys.exit, 0)


