import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Format, Const

from dviu_timetable.bot.onboarding.states import OnboardingState

_logger = logging.getLogger(__name__)


async def role_select_callback(callback: CallbackQuery, _: Button, manager: DialogManager):
    manager.dialog_data['selected_role'] = callback.data

    if callback.data == 'student':
        manager.dialog_data['human_readable_role'] = 'Студент'
        await manager.switch_to(OnboardingState.STUDENT_SELECT_FACULTY)

    elif callback.data == 'teacher':
        manager.dialog_data['human_readable_role'] = 'Преподаватель'
        await manager.switch_to(OnboardingState.TEACHER_SELECT)

    else:
        raise RuntimeError('We\'re fucked (2)')


async def create_role_select_window():
    return Window(
        Format('✅ <b>{dialog_data[human_readable_domain]}</b>'),
        Format('➡️ <b>Выбор роли</b>\n'),
        Const('Кто ты?'),
        Button(Const('Я студент 🧑‍🎓'), id='student', on_click=role_select_callback),
        Button(Const('Я преподаватель 🧑‍🏫'), id='teacher', on_click=role_select_callback),
        Back(Const('⬅️ Назад')),

        state=OnboardingState.SELECT_ROLE
    )
