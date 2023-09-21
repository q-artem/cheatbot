import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from configs import *
import global_variables
from config_reader import config
from utils import get_value_from_id, debug, add_user, write_value_from_id
from functions import service_block, set_watch, send_cheats, set_settings


if ENABLE_PROXY:
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML", session=session)  # Объект бота
else:
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")

logging.basicConfig(level=logging.INFO)  # Включаем логирование, чтобы не пропустить важные сообщения
dp = Dispatcher()  # Диспетчер


async def main():  # Запуск процесса поллинга новых апдейтов
    global_variables.states.update({q[0]: IN_SLEEP_STATE for q in await get_value_from_id(None, fields="id", get_all=True)})
    debug("users in bd:", (", ".join([str(q) for q in global_variables.states.keys()])))
    print(global_variables.states)
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
    keyboard = types.ReplyKeyboardMarkup(keyboard=keyboards[IN_SLEEP_STATE], resize_keyboard=True)
    if await get_value_from_id(callback.from_user.id) is None:  # если первый раз - привет и добавляем
        await add_user(callback.from_user.id)
        await callback.message.answer(
            hiMess2.replace("Привет",
                            f"Привет! Вы уже {await get_value_from_id(None, fields='id', get_all=True)}й человек, "
                            f"который читает это", 1).replace("[separator]",
                                                              await get_value_from_id(callback.from_user.id,
                                                                                      fields="separator")),
            reply_markup=keyboard)
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
    if await get_value_from_id(message.from_user.id, fields="agreementWithDisclaimer") != 1:
        await message.answer(f"Согласитесь с условиями использования.\nОтправить повторно - /start")
        return

    debug(f"Input message from user {message.from_user.id}:\n", message.text.replace("\n", "\\n"))

    if await service_block(message):
        return True

    if await set_watch(message):
        return True

    if await set_settings(message):
        return True

    if await send_cheats(message):
        return True


if __name__ == "__main__":
    asyncio.run(main())
