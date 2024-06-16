from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


#backend for inline keybaord 

class MyCallback(CallbackData, prefix = "my"):
    foo : str
    bar : int


testingKB = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text="Tutor Mode", callback_data= "tutor"),
            InlineKeyboardButton(text="Student Mode", callback_data= "student")
        ]
    ]
)



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
tutor_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text= "Check Subjects!", callback_data=("check_subject")),
            InlineKeyboardButton(text= "Admin info!", callback_data=("hello1")),
            InlineKeyboardButton(text= "Student List", callback_data=("check_student"))
            

        ],
        [
            InlineKeyboardButton(text= "Create_subject", callback_data=("create_sub"))

        ]
    ]
)


# subject code enter command
subject_ikb = InlineKeyboardMarkup(

    inline_keyboard=
    [
        [
            InlineKeyboardButton(text= "Create a new subject", callback_data="sub_input")
        ]

    ]
)