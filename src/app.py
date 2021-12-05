import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from util import get_storage_file_path
from handler import *


class App:

    def __init__(self):
        load_dotenv()

        self.BOT_TOKEN = os.getenv("BOT_TOKEN")

        STORAGE_PATH = get_storage_file_path()
        with open(STORAGE_PATH, "a+"):
            pass

    async def _process(self):
        bot = Bot(token=self.BOT_TOKEN)
        try:
            disp = Dispatcher(bot=bot)
            disp.register_message_handler(
                start_handler, commands={"start", "restart"})
            await disp.start_polling()
        finally:
            await bot.close()

    def run(self):
        asyncio.run(self._process())
