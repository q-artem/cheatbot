import asyncio
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
import aiogram.utils.markdown as fmt

import global_variables
from configs import CHOOSING_WATCH_TEXT, IN_CHOICE_WATCH_STATE, IN_SLEEP_STATE, BACK_TEXT, SETTINGS_TEXT, \
    IN_SETTINGS_STATE, IN_SENDING_MESSAGES_STATE, IN_PREPARING_TO_SENDING_STATE, keyboards, HI_MES2, \
    REVERSE_OR_STRAIGHT_SENDING_TEXT, \
    MAX_QUANTITY_MESSAGES, SET_SEPARATOR_MESSAGES_TEXT, IN_SET_SEPARATOR_MESSAGES_STATE, MAX_LEN_SEP, \
    IN_SET_TIME_BETWEEN_MESSAGES_STATE, SET_TIME_BETWEEN_MESSAGES_TEXT, MIN_TIME_BETWEEN_MESSAGES, \
    MAX_TIME_BETWEEN_MESSAGES, SET_TIME_BEFORE_SENDING_TEXT, IN_SET_TIME_BEFORE_SENDING_STATE, \
    MIN_TIME_BEFORE_MESSAGES, MAX_TIME_BEFORE_MESSAGES, SPLIT_BY_NEW_LINE_TEXT, RESTART_THE_BOT_TEXT, \
    TAG_FOR_SEPARATOR_END, TAG_FOR_SEPARATOR_START
from utils import update_keyboard, get_value_from_id, write_value_from_id, cut_into_messages, debug, \
    create_inline_button, add_user, enter_bd_request


async def dev_block(message: types.Message):
    if message.from_user.id != 1722948286:
        return False

    if message.text.lower() == "здохни":
        await message.answer('Okk')
        exit(0)

    if message.text == "Пакажи айдишки":
        mes = [fmt.hcode(str(q[0])) + (lambda x: " : (" + str(x.user.username) + ")\n" +
                                                 str(x.user.first_name) + " " + str(x.user.last_name))(
            await global_variables.bot_lc.get_chat_member(q[0], q[0])).replace("None", "[?]")
               for q in await get_value_from_id(None, fields="id", get_all=True)]
        debug(mes)
        await message.answer("\n".join(mes))
        return True

    spl = message.text.split(" ")
    if len(spl) > 2 and spl[0].lower() == "bd":
        idq = await enter_bd_request(" ".join(spl[1:]))
        if idq[0]:
            await message.answer("Удачно!\n" + "\n".join(
                ("(" + ", ".join(["<code>" + str(w) + "</code>" for w in q]) + ")" for q in idq[1])))
        else:
            await message.answer("Неудачно! Ошибка:\n" + str(idq[1]))
        return True

    if len(spl) > 2 and spl[0].lower() == "snd" and spl[1].isdigit():
        idq = int(spl[1])
        try:
            await global_variables.bot_lc.send_message(idq, " ".join(spl[2:]))
        except TelegramBadRequest as e:
            await message.answer("Какая то ошибка: " + str(e))
            return True
        await message.answer("Готово!")
        return True


async def service_block(message: types.Message):
    if message.text == CHOOSING_WATCH_TEXT:
        global_variables.states[message.from_user.id] = IN_CHOICE_WATCH_STATE
        await message.answer('Выберите свои часы из меню:',
                             reply_markup=await update_keyboard(message, is_watches_keyboard=True))
        return True

    if message.text == SETTINGS_TEXT:
        global_variables.states[message.from_user.id] = IN_SETTINGS_STATE
        await message.answer('Выберите параметр из меню:', reply_markup=await update_keyboard(message))
        return True

    if message.text == RESTART_THE_BOT_TEXT:
        await send_hi_message(message, False)
        return True

    if message.text == BACK_TEXT and (global_variables.states[message.from_user.id] == IN_CHOICE_WATCH_STATE or
                                      global_variables.states[message.from_user.id] == IN_SETTINGS_STATE):
        global_variables.states[message.from_user.id] = IN_SLEEP_STATE
        await message.answer('Готов к работе!', reply_markup=await update_keyboard(message))
        return True

    if message.text == BACK_TEXT and \
            (global_variables.states[message.from_user.id] == IN_SET_SEPARATOR_MESSAGES_STATE or
             global_variables.states[message.from_user.id] == IN_SET_TIME_BETWEEN_MESSAGES_STATE or
             global_variables.states[message.from_user.id] == IN_SET_TIME_BEFORE_SENDING_STATE):
        global_variables.states[message.from_user.id] = IN_SETTINGS_STATE
        await message.answer('Выберите параметр из меню:', reply_markup=await update_keyboard(message))
        return True

    if message.text == 'Моего браслета нет в списке':
        await message.answer(
            'Ой, не, ну а чего ты хотел, чтобы ещё и сторонние браслеты добавлять? Может потом сделаю')
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

    if message.text == REVERSE_OR_STRAIGHT_SENDING_TEXT:
        snd = await get_value_from_id(message.from_user.id, fields="inverseSending")
        await write_value_from_id(message.from_user.id, "inverseSending", int(not snd))
        await message.answer('Готово!\nСообщения будут отсылаться ' + ["в обратном порядке",
                                                                       "в прямом порядке (по умолчанию)"][snd])
        return True

    if message.text == SET_SEPARATOR_MESSAGES_TEXT:
        global_variables.states[message.from_user.id] = IN_SET_SEPARATOR_MESSAGES_STATE
        await message.answer(f'Введите новый разделитель текста или выберите из меню, максимум {MAX_LEN_SEP} символов '
                             f'(текущий "{await get_value_from_id(message.from_user.id, fields="separator")}"):',
                             reply_markup=await update_keyboard(message))
        return True

    if message.text == SET_TIME_BETWEEN_MESSAGES_TEXT:
        global_variables.states[message.from_user.id] = IN_SET_TIME_BETWEEN_MESSAGES_STATE
        await message.answer(f'Введите новое время в секундах между отправкой сообщений или выберите из меню, минимум '
                             f'{MIN_TIME_BETWEEN_MESSAGES}, максимум {MAX_TIME_BETWEEN_MESSAGES} (сейчас '
                             f'{await get_value_from_id(message.from_user.id, fields="timeBetweenMessages")}):',
                             reply_markup=await update_keyboard(message))
        return True

    if message.text == SET_TIME_BEFORE_SENDING_TEXT:
        global_variables.states[message.from_user.id] = IN_SET_TIME_BEFORE_SENDING_STATE
        await message.answer(f'Введите новое время в секундах перед отправкой сообщений или выберите из меню, минимум '
                             f'{MIN_TIME_BEFORE_MESSAGES}, максимум {MAX_TIME_BEFORE_MESSAGES} (сейчас '
                             f'{await get_value_from_id(message.from_user.id, fields="timeBeforeSending")}):',
                             reply_markup=await update_keyboard(message))
        return True

    await message.answer('Для возврата в главное меню нажмите кнопку "Назад"')
    return False


async def set_settings_lv2(message: types.Message):
    if global_variables.states[message.from_user.id] != IN_SET_SEPARATOR_MESSAGES_STATE and \
            global_variables.states[message.from_user.id] != IN_SET_TIME_BETWEEN_MESSAGES_STATE and \
            global_variables.states[message.from_user.id] != IN_SET_TIME_BEFORE_SENDING_STATE:
        return False

    if global_variables.states[message.from_user.id] == IN_SET_SEPARATOR_MESSAGES_STATE:
        if message.text == SPLIT_BY_NEW_LINE_TEXT:
            await write_value_from_id(message.from_user.id, "separator", "\n")
        else:
            await write_value_from_id(message.from_user.id, "separator", message.text[:MAX_LEN_SEP].replace("\n", ""))
        global_variables.states[message.from_user.id] = IN_SETTINGS_STATE
        await message.answer('Готово! Разделитель текста изменён на "{}"'.format((await get_value_from_id(
            message.from_user.id, fields="separator")).replace("\n", "[новая строка]")),
                             reply_markup=await update_keyboard(message))
        return True

    if global_variables.states[message.from_user.id] == IN_SET_TIME_BETWEEN_MESSAGES_STATE:
        if message.text.isdigit() or (len(message.text.split(".")) == 2 and message.text.split(".")[0].isdigit() and
                                      message.text.split(".")[1]):
            await write_value_from_id(message.from_user.id, "timeBetweenMessages",
                                      float(max(min(MAX_TIME_BETWEEN_MESSAGES, round(float(message.text), 2)),
                                                MIN_TIME_BETWEEN_MESSAGES)))
            global_variables.states[message.from_user.id] = IN_SETTINGS_STATE
            await message.answer(f'Готово! Время между отправкой сообщений изменено на '
                                 f'{await get_value_from_id(message.from_user.id, fields="timeBetweenMessages")} '
                                 f'секунд', reply_markup=await update_keyboard(message))
        else:
            await message.answer('Ошибка! Введено неверное время. Для возврата в главное меню нажмите кнопку "Назад"')
        return True

    if global_variables.states[message.from_user.id] == IN_SET_TIME_BEFORE_SENDING_STATE:
        if message.text.isdigit() or (len(message.text.split(".")) == 2 and message.text.split(".")[0].isdigit() and
                                      message.text.split(".")[1]):
            await write_value_from_id(message.from_user.id, "timeBeforeSending",
                                      float(max(min(MAX_TIME_BEFORE_MESSAGES, round(float(message.text), 2)),
                                                MIN_TIME_BEFORE_MESSAGES)))
            global_variables.states[message.from_user.id] = IN_SETTINGS_STATE
            await message.answer(f'Готово! Время перед отправкой сообщений изменено на '
                                 f'{await get_value_from_id(message.from_user.id, fields="timeBeforeSending")} '
                                 f'секунд', reply_markup=await update_keyboard(message))
        else:
            await message.answer('Ошибка! Введено неверное время. Для возврата в главное меню нажмите кнопку "Назад"')
        return True

    await message.answer('Для возврата в главное меню нажмите кнопку "Назад"')
    return False


async def send_cheats(message: types.Message):
    if global_variables.states[message.from_user.id] != IN_SLEEP_STATE and \
            global_variables.states[message.from_user.id] != IN_PREPARING_TO_SENDING_STATE:
        return True
    first_call = True
    if message.from_user.id in global_variables.inputs.keys():
        first_call = False
    else:
        global_variables.inputs[message.from_user.id] = ""

    global_variables.inputs[message.from_user.id] += message.text
    watch_id, separator, reverse = await get_value_from_id(message.from_user.id,
                                                           fields="selectedWatch, separator, inverseSending")
    local_separator = (None, False)
    if TAG_FOR_SEPARATOR_START in global_variables.inputs[message.from_user.id] and \
            TAG_FOR_SEPARATOR_END in global_variables.inputs[message.from_user.id]:
        curr_text = global_variables.inputs[message.from_user.id]
        local_separator = (curr_text[curr_text.find(TAG_FOR_SEPARATOR_START) + len(TAG_FOR_SEPARATOR_START):
                                     curr_text.find(TAG_FOR_SEPARATOR_END)], True)
        if len(local_separator[0]) > 0:
            global_variables.inputs[message.from_user.id] = curr_text[:curr_text.find(TAG_FOR_SEPARATOR_START)] + \
                                                            curr_text[curr_text.find(TAG_FOR_SEPARATOR_END) + len(
                                                                              TAG_FOR_SEPARATOR_END):]
        else:
            local_separator = (None, False)
    if local_separator[1]:
        separator = local_separator[0]

    is_quantity_messages_highest = ""
    quantity_messages_no_split_max = len([1 for q in
                                          (await cut_into_messages(watch_id, separator,
                                                                   global_variables.inputs[message.from_user.id]
                                                                   )) if q != ""])
    quantity_messages = min(MAX_QUANTITY_MESSAGES, quantity_messages_no_split_max)  # не больше скольки то уведомлений
    quantity_messages_word = (lambda x: ("е" + "я" * 3 + "й" * 6)[(x - 1) % 10])(quantity_messages)
    if quantity_messages_no_split_max > MAX_QUANTITY_MESSAGES:
        is_quantity_messages_highest = "первые "
    if first_call:
        global_variables.states[message.from_user.id] = IN_PREPARING_TO_SENDING_STATE
        seconds_before = (lambda x: [x, int(x)][x.is_integer()])(await get_value_from_id(message.from_user.id,
                                                                                         fields="timeBeforeSending"))
        seconds_between = (lambda x: [x, int(x)][x.is_integer()])(await get_value_from_id(message.from_user.id,
                                                                                          fields="timeBetweenMessages"))
        seconds_before_word = (lambda x: ("у" + "ы" * 3 + "д" * 6)[(x - 1) % 10])(
            int(str(seconds_before).split(".")[-1])).replace("д", "")
        seconds_between_word = (lambda x: ("у" + "ы" * 3 + "д" * 6)[(x - 1) % 10])(
            int(str(seconds_between).split(".")[-1])).replace("д", "")
        reverse_word = (lambda x: ["", " в обратном порядке"][x])(reverse)  # нормальные секунды ^
        local_separator_word = "\nЛокальный разделитель: " + '"' + str(local_separator[0]).replace("\n", "\\n") + '"'
        await message.answer(
            f'Принято, отправлю {is_quantity_messages_highest}{quantity_messages} сообщени{quantity_messages_word} '
            f'через {seconds_before} секунд{seconds_before_word} c интервалом в {seconds_between} '
            f'секунд{seconds_between_word}{reverse_word} на браслет '
            + await get_value_from_id(watch_id, table="watches", fields="name") + "."
            f'{local_separator_word * (local_separator[1] == True)}' +
            "\n\nЗакройте чат или выйдите из приложения", reply_markup=await create_inline_button("Отменить отправку",
                                                                                                  "cansel_sending"))
        await asyncio.sleep(2)  # пока задержка, досылаются сообщения
        debug(f"Preparing to sending to user {message.from_user.id}...")
        await asyncio.sleep(await get_value_from_id(
            message.from_user.id, fields="timeBeforeSending") - 2)  # пока задержка, досылаются сообщения
        split_messages = await cut_into_messages(watch_id, separator, global_variables.inputs[message.from_user.id])
        split_messages = split_messages[:MAX_QUANTITY_MESSAGES]
        global_variables.inputs.pop(message.from_user.id)
        if global_variables.states[message.from_user.id] == IN_PREPARING_TO_SENDING_STATE:
            global_variables.states[message.from_user.id] = IN_SENDING_MESSAGES_STATE
        else:
            debug("Sending interrupted!")
            return True
        if reverse:
            split_messages = split_messages[::-1]
        while len(split_messages) > 0:
            if global_variables.states[message.from_user.id] != IN_SENDING_MESSAGES_STATE:
                break
            if split_messages[0] == "":  # не помню зачем, но не повредит
                split_messages.pop(0)
                continue
            debug(f"Sending to user {message.from_user.id}... {len(split_messages) - 1} left\n",
                  split_messages[0].replace("\n", "\\n"))
            await message.answer(split_messages[0].replace("<", "&lt;"))
            split_messages.pop(0)
            if len(split_messages) != 0:  # чтобы в конце не было задержки
                await asyncio.sleep(seconds_between)
        else:
            debug("Pass!")
            global_variables.states[message.from_user.id] = IN_SLEEP_STATE
            return True
        debug("Sending interrupted!")
    else:
        await message.answer(
            f'Добавлено ещё одно сообщение, будут отправлены {is_quantity_messages_highest}{quantity_messages} '
            f'сообщени{quantity_messages_word}')
        debug(f"Added 1 message from user {message.from_user.id}, will be send {quantity_messages} messages")
    return True


async def send_hi_message(message: types.Message, is_first_start: bool):
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards[IN_SLEEP_STATE], resize_keyboard=True)
    try:
        global_variables.inputs.pop(message.chat.id)  # если перезапустили
    except KeyError:
        pass
    try:
        global_variables.states[message.chat.id] = IN_SLEEP_STATE  # добавим в список юзеров в переменной
    except KeyError:
        pass
    if is_first_start:  # если первый раз - привет и добавляем
        await add_user(message.chat.id)
        await message.answer(
            HI_MES2.replace("Привет",
                            f"Привет! Вы уже {len(await get_value_from_id(None, fields='id', get_all=True))}й человек, "
                            f"который читает это", 1).replace("[separator]",
                                                              await get_value_from_id(message.chat.id,
                                                                                      fields="separator")),
            reply_markup=keyboard)
        await write_value_from_id(message.chat.id, "agreementWithDisclaimer", 1)
    else:
        await message.answer(  # если нет - привет снова
            HI_MES2.replace("Привет", "С возвращением", 1).replace("[separator]",
                                                                   await get_value_from_id(message.chat.id,
                                                                                           fields="separator")),
            reply_markup=keyboard)
