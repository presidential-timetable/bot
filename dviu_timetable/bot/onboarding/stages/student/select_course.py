import logging
import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Button, Select, Column
from aiogram_dialog.widgets.text import Format, Const

from dviu_timetable.bot.onboarding.states import OnboardingState
from dviu_timetable.core.models.course import Course
from dviu_timetable.core.providers.impl.group_provider import GroupProviderImpl

_logger = logging.getLogger(__name__)


async def _course_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "courses": [
            (course.course_name, course.course_id)
            for course in dialog_manager.dialog_data['meta_provider'].get_courses()
        ]
    }


async def _course_select_callback(_: CallbackQuery, __: Button, manager: DialogManager, item_id: str):
    course: Course = manager.dialog_data['meta_provider'].get_course_by_id(int(item_id))

    manager.dialog_data['selected_course'] = course  # noqa
    manager.dialog_data['human_readable_course'] = course.course_name  # noqa

    manager.dialog_data['group_provider'] = GroupProviderImpl(
        domain=manager.dialog_data['selected_domain'],
        domain_provider=manager.start_data['domain_provider'],
        meta_provider=manager.dialog_data['meta_provider']
    )

    await manager.next()


async def create_course_select_window():
    return Window(
        Format('✅ <b>{dialog_data[human_readable_domain]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_role]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_faculty]}</b>'),
        Format('➡️ <b>Выбор курса</b>\n'),
        Const('На каком курсе ты учишься?'),
        Column(
            Select(
                Format('{item[0]}'),
                id='s_courses',
                item_id_getter=operator.itemgetter(1),
                items='courses',
                on_click=_course_select_callback
            )
        ),
        Back(Const('⬅️ Назад')),

        getter=_course_getter,
        state=OnboardingState.STUDENT_SELECT_COURSE
    )
