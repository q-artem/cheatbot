import asyncio
from aiogram import types

import global_variables
from configs import CHOOSING_WATCH_TEXT, IN_CHOICE_WATCH_STATE, IN_SLEEP_STATE, BACK_TEXT, SETTINGS_TEXT, \
    IN_SETTINGS_STATE
from utils import update_keyboard, get_value_from_id, write_value_from_id, cut_into_messages, debug


async def service_block(message: types.Message):
    if message.text == "Здохни":
        await message.answer('Неа, всё, отладка больше не работает')
        return True

    if message.text == "Здохни, заклинаю":
        await message.answer('Okk')
        exit(0)

    if message.text == CHOOSING_WATCH_TEXT:
        global_variables.states[message.from_user.id] = IN_CHOICE_WATCH_STATE
        await message.answer('Выберите свои часы из меню:', reply_markup=await update_keyboard(message))
        return True

    if message.text == SETTINGS_TEXT:
        global_variables.states[message.from_user.id] = IN_SETTINGS_STATE
        await message.answer('Выберите параметр из меню:', reply_markup=await update_keyboard(message))
        return True

    if message.text == BACK_TEXT and (global_variables.states[message.from_user.id] == IN_CHOICE_WATCH_STATE or
                                      global_variables.states[message.from_user.id] == IN_SETTINGS_STATE):
        global_variables.states[message.from_user.id] = IN_SLEEP_STATE
        await message.answer('Готов к работе!', reply_markup=await update_keyboard(message))
        return True

    if message.text == 'Моего браслета нет в списке':
        await message.answer(
            'Ой, не, ну а чего ты хотел, чтобы ещё и сторонние браслеты добавлять? '
            'Мне за это не платят. Может потом сделаю')
        return True
    return False


async def set_watch(message: types.Message):
    if global_variables.states[message.from_user.id] != IN_CHOICE_WATCH_STATE:
        return False
    if not await get_value_from_id(message.text, table="watches", fields="id", sign_column="name") is None:
        await write_value_from_id(
            message.from_user.id, "selectedWatch", await get_value_from_id(
                message.text, table="watches", fields="id", sign_column="name"))
        global_variables.states[message.from_user.id] = IN_SLEEP_STATE
        await message.answer('Принято.\nГотов к работе!', reply_markup=await update_keyboard(message))
        return True
    await message.answer('Сначала выберите часы из меню или вернитесь назад')
    return False


async def set_settings(message: types.Message):
    if global_variables.states[message.from_user.id] != IN_SETTINGS_STATE:
        return False

    pass

    await message.answer('Сорян, пока без настроек')
    return False


async def send_cheats(message: types.Message):
    if global_variables.states[message.from_user.id] != IN_SLEEP_STATE:
        return True
    first_call = True
    if message.from_user.id in global_variables.inputs.keys():
        first_call = False
    else:
        global_variables.inputs[message.from_user.id] = ""

    global_variables.inputs[message.from_user.id] += message.text
    watch_id, separator, reverse = await get_value_from_id(message.from_user.id,
                                                           fields="selectedWatch, separator, inverseSending")
    quantity_messages = len(
        [1 for q in (await cut_into_messages(watch_id, separator, global_variables.inputs[message.from_user.id])) if
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
        split_messages = await cut_into_messages(watch_id, separator, global_variables.inputs[message.from_user.id])
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
        global_variables.inputs.pop(message.from_user.id)
        debug("Pass!")
    else:
        await message.answer(
            f'Добавлено ещё одно сообщение, будет отправлено {quantity_messages} сообщени{quantity_messages_word}')
        debug(f"Added 1 message from user {message.from_user.id}, will be send {quantity_messages} messages")
    return True
