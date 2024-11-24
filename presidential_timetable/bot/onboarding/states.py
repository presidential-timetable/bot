from aiogram.fsm.state import StatesGroup, State


class OnboardingState(StatesGroup):
    MAIN = State()
    USER_TYPE = State()
    TEACHER_SELECT = State()
    STUDENT_GROUP_SELECT = State()
