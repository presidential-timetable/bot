import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from aiogram_dialog import (
    DialogManager, setup_dialogs, StartMode
)

from presidential_timetable.bot.onboarding.dialog import make_onboarding_dialog

from presidential_timetable.bot.onboarding.states import OnboardingState

from dotenv import load_dotenv
load_dotenv()

def setup_logging():
    logging_date_format = '%d.%m.%Y %H:%M:%S'
    logging_format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'

    logging_handlers = [
        logging.FileHandler('pt_bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]

    logging.basicConfig(
        format=logging_format,
        datefmt=logging_date_format,
        handlers=logging_handlers,
        level=logging.DEBUG
    )

    return


async def main():
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info('-*- Welcome to presidential-timetable bot! -*-')

    storage = MemoryStorage()
    bot = Bot(
        token=os.getenv('PT_BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        await make_onboarding_dialog()
    )

    setup_dialogs(dp)

    @dp.message(Command("start"))
    async def start(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(OnboardingState.MAIN, mode=StartMode.RESET_STACK)

    logger.info('Starting polling...')
    await dp.start_polling(bot, skip_updates=True)
    logger.info('-*- Shutting down polling... -*-')
    return


if __name__ == '__main__':
    asyncio.run(main())
