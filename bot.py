import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import sqlite3

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from configs import *
from utils import *
from config_reader import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# Диспетчер
dp = Dispatcher()

# подключение к бд
bd = sqlite3.connect("users_info.sqlite")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Я согласен и беру ответственность на себя",
        callback_data="agreement_with_the_disclaimer")
    )
    await message.answer(
        disclaimer,
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "agreement_with_the_disclaimer")
async def send_hi_message(callback: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards["mainMenu"], resize_keyboard=True)
    if await getValueFromId(callback.from_user.id) is None:
        await callback.message.answer(hiMess2, reply_markup=keyboard) # если первый раз - привет и добавляем
        await addUser(callback.from_user.id)
    else:
        await callback.message.answer(hiMess2.replace("Привет", "С возвращением", 1).replace("[separator]", await getValueFromId(callback.from_user.id, fields="separator")), reply_markup=keyboard)  # если нет - привет сновa
    await writeValueFromId(callback.from_user.id, "agreementWithDisclaimer", 1)
    print(callback.from_user.id)
    await callback.answer()

inputs = {}

@dp.message(F.text)
async def message_handler(message: types.Message):
    print(bd.cursor().execute(f"""SELECT {"*"} FROM {"users"} WHERE id = {6526631273}""").fetchone())
    if await getValueFromId(message.from_user.id, fields="agreementWithDisclaimer") == 0:
        await message.answer(f"Согласитесь с условиями использования.\nОтправить повторно - /start")
        return

    if message.text == "Здохни":
        await message.answer('Неа, всё, отладка больше не работает')
        return

    if message.text == "Здохни, заклинаю":
        await message.answer('Okk')
        exit(0)

    if not await getValueFromId(message.text, table="watches", fields="id", sign_column="name") is None:
        return
        await writeValueFromId(message.from_user.id, "selectedWatch", await getValueFromId(message.text, table="watches", fields="id", sign_column="name"))
        await message.answer('Принято')
        return

    if message.text == 'Моего браслета нет в списке':
        await message.answer('Ойй, не, ну а чего ты хотел, чтобы ещё и сторонние браслеты добавлять? Мне за это не платят. Может потом сделаю')
        return

    firstCall = True
    if message.from_user.id in inputs.keys():
        firstCall = False
    else:
        inputs[message.from_user.id] = ""

    inputs[message.from_user.id] += message.text

    watch_id, separator, reverse = await getValueFromId(message.from_user.id, fields="selectedWatch, separator, inverseSending")
    quantity_messages = len([1 for q in (await CutIntoMessages(watch_id, message.from_user.id, separator, inputs[message.from_user.id])) if q != ""])
    quantity_messages_word = (lambda x: ("е" + "я" * 3 + "й" * 6)[(x - 1) % 10])(quantity_messages)
    if firstCall:
        seconds_before = await getValueFromId(message.from_user.id, fields="timeBeforeSending")
        seconds_between = await getValueFromId(message.from_user.id, fields="timeBetweenMessages")
        seconds_before_word = (lambda x: ("у" + "ы" * 3 + "д" * 6)[(x - 1) % 10])(seconds_before).replace("д", "")  # нормальные секунды
        seconds_between_word = (lambda x: ("у" + "ы" * 3 + "д" * 6)[(x - 1) % 10])(seconds_between).replace("д", "")
        reverse_word = (lambda x: ["", " в обратном порядке"][x])(reverse)
        await message.answer(f'Принято, отправлю {quantity_messages} сообщени{quantity_messages_word} через {seconds_before} секунд{seconds_before_word} c интервалом в {seconds_between} секунд{seconds_between_word}{reverse_word} на браслет ' + await getValueFromId(watch_id, table="watches", fields="name"))
        await asyncio.sleep(2)  # пока задержка, досылаются сообщения
        print("Preparing to sending...")
        await asyncio.sleep(await getValueFromId(message.from_user.id, fields="timeBeforeSending") - 2)  # пока задержка, досылаются сообщения

        split_messages = await CutIntoMessages(watch_id, message.from_user.id, separator, inputs[message.from_user.id])
        if reverse:
            split_messages = split_messages[::-1]
        while len(split_messages) > 0:
            if split_messages[0] == "":  # не помню зачем, но не повредит
                split_messages.pop(0)
                continue
            print(f"Sending... {len(split_messages) - 1} left\n", split_messages[0].replace("\n", "\\n"))
            await message.answer(split_messages[0])
            split_messages.pop(0)
            if len(split_messages) != 0:  # чтобы в конце не было задержки
                await asyncio.sleep(seconds_between)
        inputs.pop(message.from_user.id)
        print("Pass!")
    else:
        await message.answer(f'Добавлено ещё одно сообщение, будет отправлено {quantity_messages} сообщени{quantity_messages_word}')


    #await message.answer(f"{message.text}\n\n{52435}", parse_mode="HTML")

if __name__ == "__main__":
    asyncio.run(main())