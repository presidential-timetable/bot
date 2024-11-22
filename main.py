import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from aiogram_dialog import (
    Dialog, DialogManager, setup_dialogs, StartMode, Window,
)

from dotenv import load_dotenv
load_dotenv()

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

logger = logging.getLogger(__name__)

logger.info('-*- Welcome to presidential_timetable.bot! -*-')

storage = MemoryStorage()
bot = Bot(token=os.getenv('PT_BOT_TOKEN'))
dp = Dispatcher(storage=storage)
# INCLUDE DIALOGS HERE: dp.include_router(dialog)
setup_dialogs(dp)


@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


if __name__ == '__main__':
    logger.info('Starting polling...')
    dp.run_polling(bot, skip_updates=True)
    logger.info('-*- Shutting down polling... -*-')
