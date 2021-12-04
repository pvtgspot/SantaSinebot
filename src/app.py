import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handler import *


class App:

    def __init__(self):
        load_dotenv()

        self.BOT_TOKEN = os.getenv("BOT_TOKEN")

        STORAGE_FILE = os.environ.get("STORAGE_FILE")
        with open(STORAGE_FILE, "a+"):
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
