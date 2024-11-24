from aiogram.types import CallbackQuery
from aiogram_dialog import (
    Dialog, Window, DialogManager, ShowMode
)

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Back, Next, SwitchTo

from presidential_timetable.client.domain_factory import DomainFactory

from .states import OnboardingState


async def domain_button_callback(
        callback: CallbackQuery, button: Button, manager: DialogManager
):
    await callback.answer(f'Did select domain: {callback.data}')
    domain_id = int(callback.data.split('.')[-1])
    domain = await DomainFactory().get_domain_by_id(domain_id)
    manager.dialog_data['selected_domain'] = domain
    manager.dialog_data['selected_domain_name'] = domain.domain_name
    await manager.next()


async def user_type_button_callback(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await callback.answer(f'Did select user type: {callback.data}')
    user_type = callback.data.split('.')[-1]  # student / teacher
    manager.dialog_data['selected_user_type'] = 'Студент' if user_type == 'student' else 'Преподаватель'
    if user_type == 'student':
        return await manager.switch_to(OnboardingState.STUDENT_GROUP_SELECT)
    else:
        return await manager.switch_to(OnboardingState.TEACHER_SELECT)


async def make_domain_buttons() -> list[Button]:
    buttons_list: list[Button] = []
    for domain in await DomainFactory().get_domains():
        buttons_list.append(
            Button(
                Const(domain.domain_name),
                id=f'pt.button.domain_selector.{domain.domain_id}',
                on_click=domain_button_callback
            )
        )

    return buttons_list


async def make_onboarding_dialog() -> Dialog:
    return Dialog(
        Window(
            Const('👋 <b>Привет, студент!</b>\n'),
            Const('Для начала, выбери учреждение, в котором ты учишься:'),
            *await make_domain_buttons(),
            state=OnboardingState.MAIN
        ),
        Window(
            Format('1️⃣✅ <b>{dialog_data[selected_domain_name]}</b>\n'),
            Format('2️⃣ Кто по масти?'),
            Button(Const('🎓 Студент'), id='pt.button.user_type.selector.student', on_click=user_type_button_callback),
            Button(Const('👤 Преподаватель'), id='pt.button.user_type.selector.teacher', on_click=user_type_button_callback),
            Back(Const('⬅️ Назад')),
            state=OnboardingState.USER_TYPE
        ),
        Window(
            Format('1️⃣✅ <b>{dialog_data[selected_domain_name]}</b>'),
            Format('2️⃣✅ <b>{dialog_data[selected_user_type]}</b>\n'),
            Const('3️⃣ Выберите себя в списке:'),
            Button(Const('Кожеуров И. В.'), id='pt.button.teacher.1'),
            Button(Const('Дагбаева А. В.'), id='pt.button.teacher.2'),
            Button(Const('абоба'), id='pt.button.teacher.3'),
            SwitchTo(Const('⬅️ Назад'), state=OnboardingState.USER_TYPE, id='pt.button.back'),
            state=OnboardingState.TEACHER_SELECT
        ),
        Window(
            Format('1️⃣✅ <b>{dialog_data[selected_domain_name]}</b>'),
            Format('2️⃣✅ <b>{dialog_data[selected_user_type]}</b>\n'),
            Const('3️⃣ Выбери свою группу:'),
            Button(Const('БД-41/11'), id='pt.button.student_group.1'),
            Button(Const('Ю-42/9'), id='pt.button.student_group.2'),
            Button(Const('опездолы'), id='pt.button.teacher.3'),
            SwitchTo(Const('⬅️ Назад'), state=OnboardingState.USER_TYPE, id='pt.button.back'),
            state=OnboardingState.STUDENT_GROUP_SELECT
        )
    )
