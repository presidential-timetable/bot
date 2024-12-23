import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Format, Const

from dviu_timetable.bot.onboarding.states import OnboardingState
from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider
from dviu_timetable.core.providers.impl.meta_provider import MetaProviderImpl

_logger = logging.getLogger(__name__)


async def domain_select_callback(callback: CallbackQuery, button: Button, manager: DialogManager):
    _logger.debug(f'domain_select_callback({callback=}, {button=}, {manager=})')
    domain = button.domain  # noqa

    manager.dialog_data['selected_domain'] = domain
    _logger.debug(f'dialog_data[selected_domain] = {domain}')

    manager.dialog_data['human_readable_domain'] = domain.domain_name
    _logger.debug(f'dialog_data[human_readable_domain] = {domain.domain_name}')

    meta_provider = MetaProviderImpl(
        domain=domain,
        domain_provider=manager.start_data['domain_provider']
    )
    manager.dialog_data['meta_provider']: MetaProviderImpl = meta_provider
    _logger.debug(f'dialog_data[meta_provider] = {meta_provider=}')

    await manager.next()


def generate_domain_buttons(domain_provider: AbstractDomainProvider):
    _logger.debug(f'generate_domain_buttons({domain_provider=})')

    for domain in domain_provider.get_domains():
        new_button = Button(
            Const(domain.domain_name),
            id=str(domain.domain_id),
            on_click=domain_select_callback
        )
        new_button.domain = domain
        yield new_button


async def create_domain_select_window(domain_provider: AbstractDomainProvider):
    return Window(
        Format(f'➡️ <b>Выбор учреждения</b>\n'),
        Const('Для начала выбери, где ты учишься 👇'),
        *list(generate_domain_buttons(domain_provider)),
        Back(Const('⬅️ Назад')),

        state=OnboardingState.SELECT_DOMAIN
    )
