import os

from pathlib import Path
from aiogram import types
from util import get_storage_file_path
from disorders import disorder
from participants import save_participants_to, load_participants_from



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

async def shuffle_handler(event: types.Message):
    STORAGE_PATH = get_storage_file_path()

    MASTER_IDS = [
        261135959, # Daniil Frangov
        426142808  # Gleb Bakhmetyev
    ]

    no_access_msg = "У вас нет прав на выполнение данной операции"
    success_msg = "Распределение сасантов успешно выполнено"

    user_id = event.from_user.id

    if MASTER_IDS.count(user_id) == 0:
        await event.answer(
            no_access_msg,
            parse_mode=types.ParseMode.HTML,
        )
        
        return

    
    with open(STORAGE_PATH, "r+") as f:
        ids = read_ids(f)
        
        shuffle = disorder(ids)    
        shuffle_ids = map(lambda x:str(x), shuffle)

        save_participants_to("shuffle", shuffle_ids)


    await event.answer(
        success_msg,
        parse_mode=types.ParseMode.HTML,
    )

async def getsome_handler(event: types.Message):
    STORAGE_PATH = get_storage_file_path()

    user_id = event.from_user.id

    msg = "Ты даришь подарок "

    ids = []
    with open(STORAGE_PATH, "r+") as f:
        ids = read_ids(f)

    shuffle_ids = load_participants_from("shuffle")

    user_id_str = str(user_id)

    i = ids.index(user_id_str)

    sasanta_id = int(shuffle_ids[i])

    sasanta_user = users.getFullUser(sasanta_id) # TODO

    sasanta_mention = sasanta_user.get_mention(as_html=True)
    msg = msg + sasanta_mention

    await event.answer(
        msg,
        parse_mode=types.ParseMode.HTML,
    )
