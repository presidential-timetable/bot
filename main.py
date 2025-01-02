import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ErrorEvent, ReplyKeyboardRemove

from aiogram_dialog import (
    DialogManager, setup_dialogs, StartMode, ShowMode
)
from aiogram_dialog.api.exceptions import UnknownIntent

from dviu_timetable.bot.onboarding.dialog import make_onboarding_dialog
from dviu_timetable.bot.main_menu.dialog import make_main_menu_dialog

from dviu_timetable.bot.onboarding.states import OnboardingState
from dviu_timetable.bot.main_menu.states import MainMenuState
from dviu_timetable.core.providers.abstract_meta_provider import AbstractMetaProvider

from dviu_timetable.core.providers.impl.domain_provider import DomainProviderImpl

from dviu_timetable.core.database.user import User
from dviu_timetable.core.providers.impl.group_provider import GroupProviderImpl
from dviu_timetable.core.providers.impl.meta_provider import MetaProviderImpl

LOGGING_FILE_PATH = 'data/dviu_timetable.bot.log'
LOGGING_DATE_FORMAT = '%d.%m.%Y %H:%M:%S'
LOGGING_FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'


def setup_logging() -> logging.Logger:
    handlers = [
        logging.FileHandler(LOGGING_FILE_PATH, encoding='UTF-8'),
        logging.StreamHandler(sys.stdout)
    ]

    logging.basicConfig(
        format=LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
        handlers=handlers,
        level=logging.DEBUG
    )

    return logging.getLogger(__name__)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)

    if event.update.callback_query:
        user_id = event.update.callback_query.message.from_user.id

        await event.update.callback_query.answer(
            "Бот был перезапущен из-за технических работ.",
        )
        if event.update.callback_query.message:
            try:  # noqa: SIM105
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever

    elif event.update.message:
        user_id = event.update.message.from_user.id
        await event.update.message.answer(
            "Бот был перезапущен из-за технических работ.",
            reply_markup=ReplyKeyboardRemove(),
        )

    else:
        raise Exception('unknown intent is very unknown blyat')

    if User.check_exists(user_id):
        await dialog_manager.start(MainMenuState.MAIN, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(OnboardingState.MAIN, mode=StartMode.RESET_STACK)

    return


async def main():
    logger = setup_logging()

    logger.info('-*- Welcome to dviu_timetable.bot! -*-')

    domain_provider = DomainProviderImpl()

    storage = MemoryStorage()
    bot = Bot(
        token='7650234499:AAH6NbbxBC4Dbz3kcZClQ6-Yg5EoIS8yEmo',
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)
    setup_dialogs(dp)

    dp.include_routers(
        await make_onboarding_dialog(domain_provider),
        await make_main_menu_dialog()
    )

    setup_dialogs(dp)
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent)
    )

    @dp.message(Command("start"))
    async def start(message: Message, dialog_manager: DialogManager):
        user_id = message.from_user.id
        if User.check_exists(user_id):
            data_dict = User.get_dict_data_by_id(user_id)

            domain = domain_provider.get_domain_by_id(data_dict['domain_id'])
            meta_provider = MetaProviderImpl(domain, domain_provider)
            group_provider = GroupProviderImpl(domain, domain_provider, meta_provider)

            user = User.get_by_id(user_id, domain_provider, meta_provider, group_provider)

            await dialog_manager.start(
                MainMenuState.MAIN,
                mode=StartMode.RESET_STACK,
                data={'user': user}
            )

        else:
            await dialog_manager.start(
                OnboardingState.MAIN,
                mode=StartMode.RESET_STACK,
                data={'domain_provider': domain_provider}
            )

    logger.info('Starting polling...')

    await dp.start_polling(bot, skip_updates=True)

    logger.info('Shutting down...')
    return


if __name__ == '__main__':
    asyncio.run(main())
