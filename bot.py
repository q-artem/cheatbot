import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import F

from configs import *
import global_variables
from config_reader import config
from utils import get_value_from_id, debug, create_inline_button
from functions import service_block, set_watch, send_cheats, set_settings, dev_block, send_hi_message

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")

logging.basicConfig(level=logging.INFO)  # Включаем логирование, чтобы не пропустить важные сообщения
dp = Dispatcher()  # Диспетчер


async def main(bot_lc1):  # Запуск процесса поллинга новых апдейтов
    global_variables.states.update({q[0]: IN_SLEEP_STATE for q in await get_value_from_id(None,
                                                                                          fields="id", get_all=True)})
    global_variables.bot_lc = bot_lc1
    debug("users in bd:", (", ".join([str(q) for q in global_variables.states.keys()])))
    try:
        await dp.start_polling(global_variables.bot_lc)
    except Exception as e:
        print("Error:", e)
        print("Using Proxy", PROXY_URL)
        session = AiohttpSession(proxy=PROXY_URL)
        global_variables.bot_lc = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML", session=session)
    await dp.start_polling(global_variables.bot_lc)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if await get_value_from_id(message.from_user.id) is None:  # если первый раз - дисклеймер
        await message.answer(disclaimer, reply_markup=await create_inline_button(
            "Я согласен и беру ответственность на себя", "agreement_with_the_disclaimer"))
    else:
        await send_hi_message(message, False)
    return True


@dp.callback_query(F.data == "agreement_with_the_disclaimer")
async def send_hi_message_handler(callback: types.CallbackQuery):
    if await get_value_from_id(callback.from_user.id) is None:  # если первый раз
        await send_hi_message(callback.message, True)
    else:
        await callback.message.answer("Вы уже согласились с условиями использования")
    await callback.answer()
    return True


@dp.callback_query(F.data == "cansel_sending")
async def stop_send_messages(callback: types.CallbackQuery):
    if global_variables.states[callback.from_user.id] == IN_SENDING_MESSAGES or \
            global_variables.states[callback.from_user.id] == IN_PREPARING_TO_SENDING:
        global_variables.states[callback.from_user.id] = IN_SLEEP_STATE
        print(callback.from_user.id, global_variables.states[callback.from_user.id])
        await callback.message.answer("Отправка сообщений отменена")
    else:
        await callback.message.answer("Сообщения сейчас не отправляются")
    await callback.answer()


@dp.message(F.text)
async def message_handler(message: types.Message):
    if await get_value_from_id(message.from_user.id, fields="agreementWithDisclaimer") != 1:
        await message.answer(f"Согласитесь с условиями использования.\nОтправить повторно - /start")
        return

    debug(f"Input message from user {message.from_user.id}:\n", message.text.replace("\n", "\\n"))

    if await dev_block(message):
        return True

    if global_variables.states[message.from_user.id] == IN_SENDING_MESSAGES:  # если работаем
        return True

    if await service_block(message):
        return True

    if await set_watch(message):
        return True

    if await set_settings(message):
        return True

    if await send_cheats(message):
        return True


if __name__ == "__main__":
    print(HI_LOGO)
    asyncio.run(main(bot))
