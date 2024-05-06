from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton



keeb = ReplyKeyboardMarkup(
keyboard=[
    [
    KeyboardButton(text = "/start"),
    KeyboardButton(text = "/reply"),
    KeyboardButton(text = "/dice")
    ],
    [
    KeyboardButton(text = "/admin_info"),
    KeyboardButton(text = "/reply"),
    KeyboardButton(text = "/dice")
    ]
    
],
resize_keyboard=True,
one_time_keyboard=True
)