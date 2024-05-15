from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


#backend for inline keybaord 

class MyCallback(CallbackData, prefix = "my"):
    foo : str
    bar : int



#keyboard demo 

    #reply keyboard
reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text = "/start"),
        KeyboardButton(text = "/reply"),
        KeyboardButton(text = "/dice")
        ],
        [
        KeyboardButton(text = "/admin_info"),
        KeyboardButton(text = "/reply")
        ]
        
    ],
    resize_keyboard=True,
    one_time_keyboard=True #hides the keyboard afer tapping one time 
)

    #inline keyboard
ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text= "Loop button!", callback_data=("hello")),
            InlineKeyboardButton(text= "Admin info!", callback_data=("hello1")),
            InlineKeyboardButton(text= "Reply keyboard demo!", callback_data=("hello2"))

        ]
    ]
)

# subject code enter command
subject_ikb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        InlineKeyboardButton(text= "Create a new subject", callback_data="sub_input")
    ]
)