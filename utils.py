import sqlite3
import time

from aiogram.utils.keyboard import InlineKeyboardBuilder

import global_variables
from configs import *

bd = sqlite3.connect("users_info.sqlite")  # подключение к бд


def debug(*args, sep=' ', end='\n', file=None):
    if ENABLE_DEBUG:
        lct = time.localtime()
        tm = (int(time.strftime("%H", lct)) - int(time.strftime("%z", lct)[1:-2]) + TIMEZONE) % 24
        print(time.strftime(f"%m/%d/%Y {(lambda x: (2 - len(str(x))) * '0' + str(x))(tm)}:%M:%S", lct) + "." +
              (str(time.time()).split(".")[-1] + "000")[:7], "->", *args, sep=sep, end=end, file=file)
        return True
    else:
        return False


async def enter_bd_request(rq: str):
    try:
        data = bd.cursor().execute(rq).fetchall()
        bd.commit()
        debug("User bd request: " + rq + " >>> " + str(data))
        return True, data
    except BaseException as e:
        debug("In", "getValueFromId", e)
        return False, e


async def get_value_from_id(idq, table="users", sign_column="id", fields="*", get_all=False):
    debug_mess = ""
    try:  # получение значения из базы
        if not get_all:
            debug_mess = """SELECT {fields} FROM {table} WHERE {sign_column} = {idq}""".format(fields=fields,
                                                                                               table=table,
                                                                                               sign_column=sign_column,
                                                                                               idq=idq, )
            data = bd.cursor().execute(
                """SELECT {fields} FROM {table} WHERE {sign_column} = ?""".format(fields=fields,
                                                                                  table=table,
                                                                                  sign_column=sign_column, ),
                (idq,)).fetchone()
        else:
            debug_mess = f'''SELECT {fields} FROM {table} >>> '''
            data = bd.cursor().execute('''SELECT {fields} FROM {table}'''.format(fields=fields,
                                                                                 table=table,
                                                                                 )).fetchall()
        if fields != "*" and len(fields.split(",")) == 1 and (not get_all):
            if data is None:
                debug(debug_mess + " >>> " + "None")
                return None
            debug(debug_mess + " >>> " + str(data[0]))
            return data[0]
        else:
            debug(debug_mess + " >>> " + str(data))
            return data
    except BaseException as e:
        debug("In", "getValueFromId", str(e) + "; request: " + debug_mess)
        return False


async def write_value_from_id(idq, fields, value, table="users"):  # изменение значения в базе
    try:
        data = bd.cursor().execute("""UPDATE {table} SET {fields} = ? WHERE id = ?""".format(table=table,
                                                                                             fields=fields,
                                                                                             ), (value, idq)).fetchone()
        bd.commit()
        debug("""UPDATE {table} SET {fields} = {value} WHERE id = {idq}""".format(table=table,
                                                                                  fields=fields,
                                                                                  value=value,
                                                                                  idq=idq))
        return data
    except BaseException as e:
        debug("In", "writeValueFromId", e)
        return False


async def add_user(idq) -> bool:  # добавление пользователя в базу данных
    try:
        bd.cursor().execute("""INSERT INTO users (id) VALUES (?)""", (idq,))
        bd.commit()
    except sqlite3.Error as e:
        debug("Ошибка записи в БД:", e)
        return False
    debug("Добавлен новый пользователь, запись в БД завершена")
    return True


async def update_keyboard(message: types.Message, is_watches_keyboard: bool = False):
    if is_watches_keyboard:
        return types.ReplyKeyboardMarkup(keyboard=await build_keyboard(), resize_keyboard=True)
    return types.ReplyKeyboardMarkup(keyboard=keyboards[global_variables.states[message.from_user.id]],
                                     resize_keyboard=True)


async def create_inline_button(text, name_funk):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=text, callback_data=name_funk))
    return builder.as_markup()


def calculate_max_length_name(text: str):
    spl = text.split(" ")
    spl1 = []
    min_m = len(text)
    while len(spl) != 1:
        spl1 = [*spl1, spl.pop(0)]
        min_m = min(max(len(" ".join(spl1)), len(" ".join(spl))), min_m)
    return min_m


async def build_keyboard():
    lst = [BACK_TEXT] + sorted([q[0] for q in await get_value_from_id(None, table="watches",
                                                                      fields="name", get_all=True)],
                               key=(lambda x: (LENS_TEXT_BUTTONS[1] - calculate_max_length_name(x)) * "a" + "b" + x))
    current_len_row = 6
    ot = []
    while current_len_row > 0:
        if len(lst) >= current_len_row:
            if LENS_TEXT_BUTTONS[current_len_row] // 2 >= calculate_max_length_name(lst[current_len_row - 1]):
                lst1 = []
                for q in range(current_len_row):
                    lst1.append(types.KeyboardButton(text=lst.pop(0)))
                ot.append(lst1)
            else:
                current_len_row -= 1
        else:
            current_len_row -= 1
    return ot


async def cut_into_messages(idq, separator, data):  # разрезаем текст на сообщения по id часов
    max_len = await get_value_from_id(idq, fields="maxLengthRussian", table="watches")
    lst = []  # сейчас сообщения длины максимум как бд минус 1
    while len(data) > max_len or separator in data:
        data = data.strip()
        if separator in data[0:max_len]:
            ind = data[0:max_len].find(separator)
            lst.append(data[0:ind])
            data = data[ind + len(separator):]
        else:
            if " " in data[0:max_len]:
                ind = 0
                for q in range(len(data[0:max_len])):
                    if data[0:max_len][q] == " ":
                        ind = q
                lst.append(data[0:ind])
                data = data[ind:]
            else:
                lst.append(data[0:max_len])
                data = data[max_len:]
    lst.append(data)
    return lst
