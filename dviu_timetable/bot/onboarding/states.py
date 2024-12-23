from aiogram.fsm.state import StatesGroup, State


class OnboardingState(StatesGroup):
    MAIN = State()

    SELECT_DOMAIN = State()
    SELECT_ROLE = State()

    STUDENT_SELECT_FACULTY = State()
    STUDENT_SELECT_COURSE = State()
    STUDENT_SELECT_GROUP = State()
    STUDENT_ENTER_NAME = State()

    TEACHER_SELECT = State()
    TEACHER_ENTER_PASSCODE = State()

    CONFIRM = State()
