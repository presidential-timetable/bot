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
from dviu_timetable.bot.onboarding.states import OnboardingState

from dviu_timetable.core.providers.impl.domain_provider import DomainProviderImpl

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


async def start_dialog(_: Message | None, dialog_manager: DialogManager):
    # TODO: after making user authentication, start menu state instead of onboarding
    await dialog_manager.start(
        OnboardingState.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND
    )


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)

    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Бот был перезапущен из-за технических работ.",
        )
        if event.update.callback_query.message:
            try:  # noqa: SIM105
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever

    elif event.update.message:
        await event.update.message.answer(
            "Бот был перезапущен из-за технических работ.",
            reply_markup=ReplyKeyboardRemove(),
        )

    await start_dialog(None, dialog_manager)


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

    dp.include_router(
        await make_onboarding_dialog(domain_provider)
    )

    setup_dialogs(dp)
    dp.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))

    @dp.message(Command("start"))
    async def start(_: Message, dialog_manager: DialogManager):
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
