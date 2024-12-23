from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.text import Format, Const

from dviu_timetable.bot.onboarding.states import OnboardingState


async def _confirm_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "domain": dialog_manager.dialog_data["selected_domain"].domain_name,
        "role": dialog_manager.dialog_data["human_readable_role"].lower(),
        "faculty": dialog_manager.dialog_data["selected_faculty"].faculty_name,
        "course": dialog_manager.dialog_data["selected_course"].course_name,
        "group": dialog_manager.dialog_data["selected_group"].group_name,
        "name": dialog_manager.dialog_data["name"]
    }


async def _custom_back_callback(_: CallbackQuery, __: Button, dialog_manager: DialogManager):
    # Needed because in the dialog window stack confirm window is below teacher states.
    # It will go to teacher passcode state if you just use back
    await dialog_manager.switch_to(OnboardingState.STUDENT_ENTER_NAME)


async def _confirm_callback(_: CallbackQuery, __: Button, dialog_manager: DialogManager):
    # write to database...
    await dialog_manager.done()
    # await dialog_manager.start()  # start menu main state


async def create_confirm_window():
    return Window(
        Format('🤔 Итак, тебя зовут <b>{name}</b>, ты <b>{role}</b> и учишься в <b>{domain}</b>'
               'на <b>{course}</b> факультета <b>{faculty}</b> в группе <b>{group}</b>.\n'),
        Const("Если всё правильно, то можем начинать! 🚀"),

        Button(Const("Начать работу ✅"), id='onboarding_confirm', on_click=_confirm_callback),
        Button(Const("⬅️ Назад"), id='back', on_click=_custom_back_callback),

        getter=_confirm_getter,
        state=OnboardingState.CONFIRM
    )
