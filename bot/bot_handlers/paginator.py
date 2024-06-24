import logging
from ..firebase.fbauth import db, id_token
from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery




items_per_page = 8

# def extract_from_db(child_name : str):
def extract_from_db(objects):

    try:
        logging.info("Attempting to fetch objects from Firebase.")
        objects = objects
        if objects.each() is None:
            logging.warning("No objects found in Firebase.")
            return []
        data = [obj.key() for obj in objects.each()]
        logging.info(f"Retrieved objects: {data}")
        return data
    except Exception as e:
        logging.error(f"Error fetching objects: {e}")
        return []

def get_page(page_number, data):
    start = page_number * items_per_page
    end = start + items_per_page
    return data[start:end]


def calculate_total_pages(objects):
    return (len(objects) + items_per_page - 1) // items_per_page

def generate_list_text(page_data):
    return "\n".join([f"{i + 1}. {item}" for i, item in enumerate(page_data)])

def create_navigation_buttons(page_number : int, total_pages : int, page_data):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if page_number > 0:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text = "Previous", callback_data=f"prev_{page_number}")])

    start_index = page_number * items_per_page
    number_buttons = [
        InlineKeyboardButton(text=str(i + 1), callback_data=f"item_{start_index + i}")
        for i in range(len(page_data))
    ]
    keyboard.inline_keyboard.append(number_buttons)

    
    if page_number < total_pages - 1:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text = "Next", callback_data=f"next_{page_number}")])


    keyboard.inline_keyboard.append([InlineKeyboardButton(text = "Return to menu", callback_data="return")])
    return keyboard

def pagination(call : CallbackQuery, key):
    # global current_page
    direction, page_number = call.data.split("_")
    if direction == "prev":
        current_page = int(page_number) - 1
    elif direction == "next": 
        current_page = int(page_number) + 1
    else:
        current_page = 0
    
    objects = extract_from_db(key)
    total_pages = calculate_total_pages(objects)
    page_data = get_page(current_page, objects)
    obj_list = generate_list_text(page_data)

    keyboard = create_navigation_buttons(current_page, total_pages, page_data)

    page = f"Page {current_page + 1}/{total_pages}\n\n{obj_list}"

    return page, keyboard

def subject_access(call : CallbackQuery, key, userID):
    index = int(call.data.split("_")[1])
    objects = extract_from_db(key)

    if index < len(objects):

        sub = objects[index]
        print(sub)
        subdata = db.child("Lecturers").child(userID).child("Subject_List").child(sub).get( id_token).val()


        subject_details = f"Name: {sub}\nSubject Code: {subdata.get("subject_code")}\nNumber of students: "

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Back", callback_data="back_toList")],
            [InlineKeyboardButton(text="Delete Subject", callback_data=f"delete_{sub}")],
            [InlineKeyboardButton(text="Edit Subject Name", callback_data=f"edit_{sub}")],
            [InlineKeyboardButton(text="Return to menu", callback_data="return")]
        ])

    return subject_details, keyboard



# def student_access(call: CallbackQuery):