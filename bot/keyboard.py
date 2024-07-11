from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData



# for simple keyboards without variable callback data
# these are mostly inline keyboard.


# Registry
register_button = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(text="Alright", callback_data="registry"),
            
        ]


    ]
)


registry = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(text="Yes", callback_data="confirm_registration"),
            InlineKeyboardButton(text="Re-enter name", callback_data="registry")
        ]


    ]
)


# admin 
admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(text= "Command List", callback_data= "admin_cmd_list")
        ],
        [
            InlineKeyboardButton(text="Users List", callback_data="check_users"),
            InlineKeyboardButton(text="Lecturers List", callback_data="check_lects")
        ],
        [
            InlineKeyboardButton(text="Edit Classroom", callback_data="edit_class")
        ],
        [
            InlineKeyboardButton(text="Add/Remove Perms", callback_data="add_remove"),
            InlineKeyboardButton(text="Log Off", callback_data="log_off")
        ]


    ]
)

    #inline keyboard
lect_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text= "Check Subjects!", callback_data=("check_subject")),
            # InlineKeyboardButton(text= "Admin info!", callback_data=("hello1")),
            InlineKeyboardButton(text= "Student List", callback_data=("check_student"))
            

        ],
        [
            InlineKeyboardButton(text= "Create subject", callback_data=("create_sub"))

        ],
        [
            InlineKeyboardButton(text= "Create announcement", callback_data=("create_announcement"))

        ]
        ,
        [
            InlineKeyboardButton(text= "About", callback_data=("lect_about"))

        ]
    ]
)

lect_ann_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
           
            InlineKeyboardButton(text= "For all students", callback_data=("general_announcement"))
            

        ],
        [
            InlineKeyboardButton(text= "For a subject", callback_data=("select_subject"))

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




student_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text= "Join class", callback_data=("join_subject")),
            InlineKeyboardButton(text= "My classes", callback_data=("student_sub"))

        ],

        [
            InlineKeyboardButton(text= "About", callback_data=("studen_about"))

        ]
    ]
)





return_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Return to menu", callback_data="return")]
    ]
)

def make_return(return_callback : str):
    button = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text="Return to menu", callback_data=return_callback)]
        ]
    )
    return button 


def retry_button(callback : str):
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Retry", callback_data=callback)]
        ]
    )
    return button
