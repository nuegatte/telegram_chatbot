from aiogram.fsm.state import State, StatesGroup


class student(StatesGroup):
    default = State()

class lecturer(StatesGroup):
    default = State()
    create_sub = State()
    check_sub = State()
    check_students = State()

