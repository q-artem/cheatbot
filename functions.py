import asyncio

from bot import inputs
from utils import *


async def service_block(message):
    if message.text == "Здохни":
        await message.answer('Неа, всё, отладка больше не работает')
        return True

    if message.text == "Здохни, заклинаю":
        await message.answer('Okk')
        exit(0)

    if message.text == 'Моего браслета нет в списке':
        await message.answer(
            'Ойй, не, ну а чего ты хотел, чтобы ещё и сторонние браслеты добавлять? '
            'Мне за это не платят. Может потом сделаю')
        return True
    return False


async def set_watch(message):
    if not await get_value_from_id(message.text, table="watches", fields="id", sign_column="name") is None:
        await write_value_from_id(
            message.from_user.id, "selectedWatch", await get_value_from_id(
                message.text, table="watches", fields="id", sign_column="name"))
        await message.answer('Принято')
        return True
    return False


async def send_cheats(message):
    first_call = True
    if message.from_user.id in inputs.keys():
        first_call = False
    else:
        inputs[message.from_user.id] = ""

    inputs[message.from_user.id] += message.text
    watch_id, separator, reverse = await get_value_from_id(message.from_user.id,
                                                           fields="selectedWatch, separator, inverseSending")
    quantity_messages = len(
        [1 for q in (await cut_into_messages(watch_id, separator, inputs[message.from_user.id])) if
         q != ""])
    quantity_messages_word = (lambda x: ("е" + "я" * 3 + "й" * 6)[(x - 1) % 10])(quantity_messages)
    if first_call:
        seconds_before = await get_value_from_id(message.from_user.id, fields="timeBeforeSending")
        seconds_between = await get_value_from_id(message.from_user.id, fields="timeBetweenMessages")
        seconds_before_word = (lambda x: ("у" + "ы" * 3 + "д" * 6)[(x - 1) % 10])(seconds_before).replace("д", "")
        seconds_between_word = (lambda x: ("у" + "ы" * 3 + "д" * 6)[(x - 1) % 10])(seconds_between).replace("д", "")
        reverse_word = (lambda x: ["", " в обратном порядке"][x])(reverse)  # нормальные секунды ^
        await message.answer(
            f'Принято, отправлю {quantity_messages} сообщени{quantity_messages_word} через {seconds_before} '
            f'секунд{seconds_before_word} c интервалом в {seconds_between} секунд{seconds_between_word}{reverse_word} '
            f'на браслет ' + await get_value_from_id(watch_id, table="watches", fields="name"))
        await asyncio.sleep(2)  # пока задержка, досылаются сообщения
        debug(f"Preparing to sending to user {message.from_user.id}...")
        await asyncio.sleep(await get_value_from_id(
            message.from_user.id, fields="timeBeforeSending") - 2)  # пока задержка, досылаются сообщения
        split_messages = await cut_into_messages(watch_id, separator, inputs[message.from_user.id])
        if reverse:
            split_messages = split_messages[::-1]
        while len(split_messages) > 0:
            if split_messages[0] == "":  # не помню зачем, но не повредит
                split_messages.pop(0)
                continue
            debug(f"Sending to user {message.from_user.id}... {len(split_messages) - 1} left\n",
                  split_messages[0].replace("\n", "\\n"))
            await message.answer(split_messages[0])
            split_messages.pop(0)
            if len(split_messages) != 0:  # чтобы в конце не было задержки
                await asyncio.sleep(seconds_between)
        inputs.pop(message.from_user.id)
        debug("Pass!")
    else:
        await message.answer(
            f'Добавлено ещё одно сообщение, будет отправлено {quantity_messages} сообщени{quantity_messages_word}')
        debug(f"Added 1 message from user {message.from_user.id}, will be send {quantity_messages} messages")
    return True
