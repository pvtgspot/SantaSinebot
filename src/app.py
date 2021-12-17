import os
import asyncio

from aiogram import types, Bot, Dispatcher
from dotenv import load_dotenv
from disorders import disorder


class SSBot:

    MESSAGES = {
        "no_access": "У вас нет прав на выполнение данной операции",
        "enrolled": "ты уже в списке участников",
        "not_enrolled": "ты теперь в списке участников Секретного Сасанты...",
        "getsome_error": "Кажется тебя нет в списке участников Сасанты",
        "getsome_success": "Ты даришь подарок ",
        "getsome_empty_shuffle": "Список сант еще не составлен, еблан",
        "shuffle_error": "Список участников пуст!",
        "shuffle_success": "Распределение сасантов успешно выполнено",
        "no_group": "На данный запрос я могу ответить только в личной беседе"

    }

    MASTER_IDS = {
        "Daniil Frangov": "261135959",
        "Gleb Bakhmetyev": "426142808",
    }

    def __init__(self):
        load_dotenv()
        self._bot_token = os.getenv("BOT_TOKEN")
        self._bot = Bot(token=self._bot_token)
        self._participants = []
        self._shuffle = []

    def _register_hadnlers(self, disp: Dispatcher):
        disp.register_message_handler(
            self.start_handler, commands={"start", "restart"}
        )
        disp.register_message_handler(
            self.shuffle_handler, commands={"shuffle"}
        )
        disp.register_message_handler(
            self.getsome_handler, commands={"getsome"}
        )

    async def _process(self):
        try:
            disp = Dispatcher(bot=self._bot)

            self._register_hadnlers(disp)

            await disp.start_polling()
        finally:
            await self._bot.close()

    async def start_handler(self, event: types.Message):
        """
        Регистрация участника
        """
        username = event.from_user.get_mention(as_html=True)

        msg = f"Привет, {username}, "

        if username not in self._participants:
            self._participants.append(username)
            msg = msg + SSBot.MESSAGES["not_enrolled"]
        else:
            msg = msg + SSBot.MESSAGES["enrolled"]

        await event.answer(
            msg,
            parse_mode=types.ParseMode.HTML,
        )

    async def shuffle_handler(self, event: types.Message):
        """
        Распределяет участников между собой
        """
        user_id = event.from_user.id

        if str(user_id) not in list(SSBot.MASTER_IDS.values()):
            await event.answer(
                SSBot.MESSAGES["no_access"],
                parse_mode=types.ParseMode.HTML,
            )

            return

        if len(self._participants) == 0:
            await event.answer(
                SSBot.MESSAGES["shuffle_error"],
                parse_mode=types.ParseMode.HTML,
            )

            return

        self._shuffle = disorder(self._participants)

        await event.answer(
            SSBot.MESSAGES["shuffle_success"],
            parse_mode=types.ParseMode.HTML,
        )

    async def getsome_handler(self, event: types.Message):
        """
        Получить сасанту санты
        """

        if event["chat"]["type"] == "group":
            await event.answer(SSBot.MESSAGES["no_group"], parse_mode=types.ParseMode.HTML,)
            return

        username = event.from_user.get_mention(as_html=True)

        if username not in self._participants or username not in self._shuffle:
            await event.answer(SSBot.MESSAGES["getsome_error"], parse_mode=types.ParseMode.HTML,)
            return

        index = self._participants.index(username)

        if len(self._shuffle) == 0:
            await event.answer(SSBot.MESSAGES["getsome_empty_shuffle"], parse_mode=types.ParseMode.HTML,)
            return

        sasanta_mention = self._shuffle[index]

        await event.answer(
            SSBot.MESSAGES["getsome_success"] + sasanta_mention,
            parse_mode=types.ParseMode.HTML,
        )

    def run(self):
        asyncio.run(self._process())
