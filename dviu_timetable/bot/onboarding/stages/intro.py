from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.text import Format, Const

from dviu_timetable.bot.onboarding.states import OnboardingState


async def create_intro_window():
    return Window(
        Format(f'👋 <b>Привет!</b>\n'),
        Const('Добро пожаловать в бот расписания ДВИУ РАНХиГС. Ну что, начнём?'),
        Next(Const('Вперёд! ➡️')),

        state=OnboardingState.MAIN
    )
