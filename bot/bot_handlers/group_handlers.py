from aiogram import Router, types , F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberAdministrator, ChatMemberOwner
from aiogram.filters import Command, Filter
from aiogram.filters.callback_data import CallbackData
from bot.config import BotConfig
from bot import keyboard
# from bot.states import student, lecturer
from aiogram.fsm.context import FSMContext
from random import randint
from ..firebase.fbauth import db, storage,id_token
import sys, logging
import asyncio
from aiogram.exceptions import TelegramNetworkError,TelegramBadRequest
from ..bot_handlers.paginator import   pagination, extract_from_db
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods.send_message import SendMessage
from aiogram.methods.create_forum_topic import CreateForumTopic
from bot_instance import bot

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
    get_user_locale
from aiogram.enums import ChatType, ChatMemberStatus
from datetime import datetime, timedelta
import os
from aiogram.methods import GetForumTopicIconStickers


group_router = Router()

class Lecturer(StatesGroup):
    default = State()
    setup = State()
    reminder = State()

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
            

class GroupChatFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}
group_router.message.filter(GroupChatFilter())


#    _____          _                   
#   / ____|        | |                  
#  | (___     ___  | |_   _   _   _ __  
#   \___ \   / _ \ | __| | | | | | '_ \ 
#   ____) | |  __/ | |_  | |_| | | |_) |
#  |_____/   \___|  \__|  \__,_| | .__/ 
#                                | |    
#                                |_|    


@group_router.message(Command("setup"))
async def pre_setup(message: types.Message, state: FSMContext):
    global user_id, bot_id, chat_id, chat_name
    user_id = message.from_user.id
    bot_id = bot.id
    chat_id = message.chat.id
    chat_name = message.chat.title
    chat_admins =await bot.get_chat_administrators(chat_id)

    bot_id = (await bot.me()).id
    is_admin = any(admin.user.id == bot_id and isinstance(admin, (ChatMemberAdministrator, ChatMemberOwner)) for admin in chat_admins)
    
    check_user = db.child("users").child(user_id).get(id_token)
    check_if_setup = db.child("Class_List").order_by_child("chat_id").equal_to(chat_id).get(id_token)

    if check_if_setup.each():

        try:
            if check_user.val() is not None:
                tutorBool = db.child("users").child(user_id).child("tutor").get(id_token)
                check_tutor = tutorBool.val()

                if check_tutor is True:
                    await state.set_state(Lecturer.default)
                    logging.info(f"Added {str(user_id)} as lecturer.")
                    
                else:
                    logging.info(f"User {str(user_id)} is not a lecturer.")
                    pass

        except TelegramBadRequest as e:
            logging.info(f"Error: {e}")    
        except Exception as e:
            logging.info(f"Error: {e}")

    else:
        if message.chat.type == ChatType.GROUP:
            error_text = (
                "You are seeing this message because\n"
                "you are not in a Super Group, but an\n"
                "ordinary Group.\n\n"
                "Here's what you can do : \n\n"
                "1. Go to the group settings.\n\n"
                "2. Click on the 'Manage Group' section.\n\n"
                "3. Toggle 'Topics' to enable it.\n\n"
                "4. Your Super Group is created! Reenter the command to redo-setup."
            )
            await message.answer(error_text)

            pass

        elif message.chat.type == ChatType.SUPERGROUP:

            if is_admin:
                try:
                    if check_user.val() is not None:
                        tutorBool = db.child("users").child(user_id).child("tutor").get(id_token)
                        check_tutor = tutorBool.val()

                        if check_tutor is True:
                            await state.set_state(Lecturer.setup)
                            setup_message = (
                                "Welcome to the setup page.\n Please enter the class enrolment code to setup.\n\n"
                                "Please make sure you have created a classroom beforehand with me in private."
                            )
                            await message.answer(setup_message)
                            await state.update_data(message=message)


                except TelegramBadRequest as e:
                    pass
                except Exception as e:
                    pass
            else:
                err = (
                    "I am not an admin in this group.\n\n"
                    "Please make me an admin and try again.\n\n"

                    "Here's what you can do : \n\n"
                    "1. Go to the group settings.\n\n"
                    "2. Click on the 'Administrators' section,\n    it is below the Topics section.\n\n"
                    "3. Add me (comm_edubot) as Admin!\n\n"
                    "4. Reenter the command to redo-setup. /setup"
                )
                await message.answer(err)
        else:
            await message.answer("You are not in a group chat. I will only function properly if you add me into a groupchat. Thank you.")


@group_router.message(Lecturer.setup)
async def setup(message: types.Message, state: FSMContext):
    enrol_code = int(message.text)
    reference = db.child("Class_List")
    existing_class = reference.order_by_child("enrol_code").equal_to(enrol_code).get(id_token)


    class_data = {
        chat_id : {
            "chat_name" : message.chat.title,
            "chat_id" : chat_id,
            "enrol_code" : enrol_code,
            
        }
    }

    chat_data = {"chat_id": chat_id}

    if existing_class.each():
        db.child("Class_List").child(enrol_code).update(chat_data, id_token)
        db.child("Chat_List").update(class_data,id_token)

        channel_list = ["FAQ", "Announcements", "Discussion Board", "Content Files","Helpdesk"]
        for channel in channel_list:
            await bot.create_forum_topic(chat_id, channel)
        await message.answer("The groupchat topics have been setup! Feel free to organise and /menu for available commands!")
        await bot.close_general_forum_topic(chat_id)
        await state.set_state(Lecturer.default)

    else : 
        await message.answer("Match not found, please re-enter the code?")



#   ______            _                          
#  |  ____|          | |                         
#  | |__  ___   __ _ | |_  _   _  _ __  ___  ___ 
#  |  __|/ _ \ / _` || __|| | | || '__|/ _ \/ __|
#  | |  |  __/| (_| || |_ | |_| || |  |  __/\__ \
#  |_|   \___| \__,_| \__| \__,_||_|   \___||___/


# @group_router.message(Command("set_announcement"))
# async def set_announcement(message: types.Message, state: FSMContext):
#     pass



@group_router.message(Command("set_announce"))
# async def date_time_input(message: types.Message, state: FSMContext):
#     await state.set_state(Lecturer.reminder)
#     await message.answer("Please enter the date and time of the announcement in the following format: YYYY-MM-DD HH:MM")
#     logging.info("State set to Lecturer.reminder")

# @group_router.message(Lecturer.reminder)
async def reminder_input(message: types.Message, state: FSMContext):
    user_input = message.text
    logging.info(f"Received user input: {user_input}")
    try:
        # reminder_time = datetime.strptime(user_input, "%Y-%m-%d %H:%M")

        reminder_time = datetime.now() + timedelta(seconds=10)
        await state.update_data(reminder_time=reminder_time)

        # Set the reminder
        asyncio.create_task(set_reminder(reminder_time, message.chat.id))

        await message.answer(f"Reminder set for {reminder_time}.")
        await state.clear()
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        await message.answer("Incorrect format. Please use 'YYYY-MM-DD HH:MM'.")

async def set_reminder(reminder_time: datetime, chat_id: int):
    current_time = datetime.now()
    time_until_reminder = reminder_time - current_time
    
   # Calculate sleep times
    sleep_2_days = (time_until_reminder - timedelta(days=2)).total_seconds()
    sleep_12_hours = (time_until_reminder - timedelta(hours=12)).total_seconds()
    sleep_5_seconds = (time_until_reminder - timedelta(seconds=5)).total_seconds()
    sleep_until_event = time_until_reminder.total_seconds()

    total = (
        f"{sleep_2_days}\n"
        f"{sleep_12_hours}\n"
        f"{sleep_5_seconds}\n"
        f"{sleep_until_event}\n"
        f"{(time_until_reminder).total_seconds()}"


    )
    logging.info(total)
    await bot.send_message(chat_id, total)

    # Send 2 days reminder if applicable
    if sleep_2_days > 0:
        await asyncio.sleep(sleep_2_days)
        await bot.send_message(chat_id, f"Reminder: Your event is in 2 days! ({reminder_time})")

    # Send 12 hours reminder if applicable
    if sleep_12_hours > 0:
        await asyncio.sleep(sleep_12_hours - sleep_2_days if sleep_2_days > 0 else sleep_12_hours)
        await bot.send_message(chat_id, f"Reminder: Your event is in 12 hours! ({reminder_time})")

    # Send 5 seconds reminder if applicable
    if sleep_5_seconds <= 5:
        valuess = sleep_5_seconds - (sleep_12_hours if sleep_12_hours > 0 else sleep_5_seconds)
        logging.info(valuess)
        await asyncio.sleep(valuess)
        await bot.send_message(chat_id, f"Reminder: Your event is in 5 seconds! ({reminder_time})")

    # Send final reminder
    if sleep_until_event > 0:
        await asyncio.sleep(sleep_until_event - (sleep_5_seconds if sleep_5_seconds > 0 else sleep_until_event))
        await bot.send_message(chat_id, f"Reminder: Your event is now! ({reminder_time})")
