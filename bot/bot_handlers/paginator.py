import logging
from ..firebase.fbauth import db, id_token
from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup



items_per_page = 8

def extract_from_db(child_name : str):
    try:
        logging.info("Attempting to fetch objects from Firebase.")
        users_snapshot = db.child(child_name).get(id_token)
        if users_snapshot.each() is None:
            logging.warning("No objects found in Firebase.")
            return []
        users = [user.key() for user in users_snapshot.each()]
        logging.info(f"Retrieved objects: {users}")
        return users
    except Exception as e:
        logging.error(f"Error fetching objects: {e}")
        return []

def get_page(page_number, data):
    start = page_number * items_per_page
    end = start + items_per_page
    return data[start:end]


def calculate_total_pages(subjects):
    return (len(subjects) + items_per_page - 1) // items_per_page

def generate_list_text(page_data):
    return "\n".join([f"{i + 1}. {item}" for i, item in enumerate(page_data)])

def create_navigation_buttons(page_number : int, total_pages : int, page_data):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if page_number > 0:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text = "Previous", callback_data=f"prev_{page_number}")])

    number_buttons = [InlineKeyboardButton(text=str(i + 1), callback_data=f"item_{i}") for i in range(len(page_data))]
    keyboard.inline_keyboard.append(number_buttons)
    
    if page_number < total_pages - 1:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text = "Next", callback_data=f"next_{page_number}")])


    keyboard.inline_keyboard.append([InlineKeyboardButton(text = "Return to menu", callback_data="return")])
    return keyboard

