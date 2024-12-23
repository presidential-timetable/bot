import logging

from aiogram_dialog import Dialog

from dviu_timetable.bot.onboarding.stages.confirm import create_confirm_window
from dviu_timetable.bot.onboarding.stages.domain_select import create_domain_select_window
from dviu_timetable.bot.onboarding.stages.intro import create_intro_window
from dviu_timetable.bot.onboarding.stages.role_select import create_role_select_window
from dviu_timetable.bot.onboarding.stages.student.enter_name import create_name_enter_window
from dviu_timetable.bot.onboarding.stages.student.select_course import create_course_select_window
from dviu_timetable.bot.onboarding.stages.student.select_faculty import create_faculty_select_window
from dviu_timetable.bot.onboarding.stages.student.select_group import create_group_select_window

from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider

_logger = logging.getLogger(__name__)

async def make_onboarding_dialog(
        domain_provider: AbstractDomainProvider
):
    _logger.debug(f'make_onboarding_dialog({domain_provider=}')

    return Dialog(
        await create_intro_window(),
        await create_domain_select_window(domain_provider),
        await create_role_select_window(),
        await create_faculty_select_window(),
        await create_course_select_window(),
        await create_group_select_window(),
        await create_name_enter_window(),
        await create_confirm_window()
    )
