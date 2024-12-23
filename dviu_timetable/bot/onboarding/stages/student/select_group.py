import logging
import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Button, Select, Column
from aiogram_dialog.widgets.text import Format, Const

from dviu_timetable.bot.onboarding.states import OnboardingState
from dviu_timetable.core.models.group import Group

_logger = logging.getLogger(__name__)


async def _group_getter(dialog_manager: DialogManager, **kwargs):
    course = dialog_manager.dialog_data['selected_course']
    faculty = dialog_manager.dialog_data['selected_faculty']

    return {
        "groups": [
            (group.group_name, group.group_id)
            for group in dialog_manager.dialog_data['group_provider'].get_groups(course, faculty)
        ]
    }


async def _group_select_callback(_: CallbackQuery, __: Button, manager: DialogManager, item_id: str):
    group: Group = manager.dialog_data['group_provider'].get_group_by_id(int(item_id))

    manager.dialog_data['selected_group'] = group  # noqa
    manager.dialog_data['human_readable_group'] = group.group_name  # noqa
    await manager.next()


async def create_group_select_window():
    return Window(
        Format('✅ <b>{dialog_data[human_readable_domain]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_role]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_faculty]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_course]}</b>'),
        Format('➡️ <b>Выбор группы</b>\n'),
        Const('В какой группе ты учишься?'),
        Column(
            Select(
                Format('{item[0]}'),
                id='s_groups',
                item_id_getter=operator.itemgetter(1),
                items='groups',
                on_click=_group_select_callback
            )
        ),
        Back(Const('⬅️ Назад')),

        getter=_group_getter,
        state=OnboardingState.STUDENT_SELECT_GROUP
    )
