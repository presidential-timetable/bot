import logging
import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Button, Select, Column
from aiogram_dialog.widgets.text import Format, Const

from dviu_timetable.bot.onboarding.states import OnboardingState
from dviu_timetable.core.models.faculty import Faculty

_logger = logging.getLogger(__name__)


async def _faculty_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "faculties": [
            (faculty.faculty_name, faculty.faculty_id)
            for faculty in dialog_manager.dialog_data['meta_provider'].get_faculties()
        ]
    }


async def _faculty_select_callback(_: CallbackQuery, __: Button, manager: DialogManager, item_id: str):
    faculty: Faculty = manager.dialog_data['meta_provider'].get_faculty_by_id(int(item_id))

    manager.dialog_data['selected_faculty'] = faculty  # noqa
    manager.dialog_data['human_readable_faculty'] = faculty.faculty_name  # noqa
    await manager.next()


async def create_faculty_select_window():
    return Window(
        Format('✅ <b>{dialog_data[human_readable_domain]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_role]}</b>'),
        Format('➡️ <b>Выбор направления</b>\n'),
        Const('На каком направлении ты учишься?'),
        Column(
            Select(
                Format('{item[0]}'),
                id='s_faculties',
                item_id_getter=operator.itemgetter(1),
                items='faculties',
                on_click=_faculty_select_callback  # noqa
            )
        ),
        Back(Const('⬅️ Назад')),

        getter=_faculty_getter,
        state=OnboardingState.STUDENT_SELECT_FACULTY
    )
