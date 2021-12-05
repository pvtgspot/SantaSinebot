import os

from pathlib import Path
from aiogram import types
from util import get_storage_file_path


def read_ids(storage_file):

    ids = storage_file.readline().strip(",")

    if len(ids) != 0:
        ids = ids.split(",")

    return ids


def write_id(storage_file, id):
    storage_file.write(f"{id},")


async def start_handler(event: types.Message):
    STORAGE_PATH = get_storage_file_path()

    user_id = event.from_user.id
    username = event.from_user.get_mention(as_html=True)

    enrolled_msg = "ты уже в списке участников"
    not_enrolled_msg = "ты теперь в списке участников Секретного Сасанты..."

    msg = f"Привет, {username}, "

    with open(STORAGE_PATH, "r+") as f:
        ids = read_ids(f)
        enrolled = False

        for id in ids:
            if int(id) == user_id:
                enrolled = True
                msg = msg + enrolled_msg
                break

        if not enrolled:
            write_id(f, user_id)
            msg = msg + not_enrolled_msg

    await event.answer(
        msg,
        parse_mode=types.ParseMode.HTML,
    )
