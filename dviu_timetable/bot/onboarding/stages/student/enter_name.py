from typing import Any

from aiogram.types import Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Format, Const

from dviu_timetable.bot.onboarding.states import OnboardingState


async def _on_name_enter_success(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        data: str
):
    dialog_manager.dialog_data['name'] = data
    await dialog_manager.switch_to(OnboardingState.CONFIRM)


async def _on_name_enter_error(message: Message,
        _: Any,
        __: DialogManager,
        ___: ValueError
):
    await message.answer('В сообщении нет пробела.')


def _name_enter_validator(message: Message) -> bool:
    return len(message.text.split()) == 2


async def create_name_enter_window():
    return Window(
        Format('✅ <b>{dialog_data[human_readable_domain]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_role]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_faculty]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_course]}</b>'),
        Format('✅ <b>{dialog_data[human_readable_group]}</b>'),
        Format('➡️ <b>Ввод имени</b>\n'),
        Const('А теперь введи своё имя и фамилию.'),
        Const('<b>ВАЖНО:</b> тебе нужно ввести их строго в формате Имя Фамилия. '),
        TextInput(
            id='student_name',
            on_error=_on_name_enter_error,
            on_success=_on_name_enter_success,
            filter=_name_enter_validator,
            type_factory=str  # TODO: maybe add a separate type?
        ),
        Back(Const('⬅️ Назад')),

        state=OnboardingState.STUDENT_ENTER_NAME
    )
