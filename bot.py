import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.client.session.aiohttp import AiohttpSession

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from configs import *
from functions import *
from config_reader import config
import sqlite3

if ENABLE_PROXY:
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML", session=session)  # Объект бота
else:
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")

logging.basicConfig(level=logging.INFO)  # Включаем логирование, чтобы не пропустить важные сообщения
dp = Dispatcher()  # Диспетчер
bd = sqlite3.connect("users_info.sqlite")  # подключение к бд
inputs = {}  # сообщения в очереди


async def main():  # Запуск процесса поллинга новых апдейтов
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Я согласен и беру ответственность на себя",
        callback_data="agreement_with_the_disclaimer")
    )
    await message.answer(disclaimer, reply_markup=builder.as_markup())


@dp.callback_query(F.data == "agreement_with_the_disclaimer")
async def send_hi_message(callback: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards["mainMenu"], resize_keyboard=True)
    if await get_value_from_id(callback.from_user.id) is None:
        await callback.message.answer(hiMess2, reply_markup=keyboard)  # если первый раз - привет и добавляем
        await add_user(callback.from_user.id)
    else:
        await callback.message.answer(  # если нет - привет снова
            hiMess2.replace("Привет", "С возвращением", 1).replace("[separator]",
                                                                   await get_value_from_id(callback.from_user.id,
                                                                                           fields="separator")),
            reply_markup=keyboard)
    await write_value_from_id(
        callback.from_user.id,
        "agreementWithDisclaimer", 1)
    debug(callback.from_user.id)
    await callback.answer()


@dp.message(F.text)
async def message_handler(message: types.Message):
    if await get_value_from_id(message.from_user.id, fields="agreementWithDisclaimer") == 0:
        await message.answer(f"Согласитесь с условиями использования.\nОтправить повторно - /start")
        return

    if await service_block(message):
        return True

    if await set_watch(message):
        return True

    if await send_cheats(message):
        return True


if __name__ == "__main__":
    asyncio.run(main())
