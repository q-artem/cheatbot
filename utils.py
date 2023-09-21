import sqlite3
import time

import global_variables
from configs import *

bd = sqlite3.connect("users_info.sqlite")  # подключение к бд


def debug(*args, sep=' ', end='\n', file=None):
    if ENABLE_DEBUG:
        print(time.strftime("%m/%d/%Y %H:%M:%S", time.localtime()) + "." + str(time.time()).split(".")[-1], "->", *args, sep=sep, end=end, file=file)
        return True
    else:
        return False


async def get_value_from_id(idq, table="users", sign_column="id", fields="*", get_all=False):
    try:                                                                          # получение значения из базы
        ggdfg = '""'
        data = None
        debug_mess = f'''SELECT {fields} FROM {table} WHERE {sign_column} = "{str(idq).replace('"', ggdfg)}" >>> '''
        if not get_all:
            data = bd.cursor().execute(f'''SELECT {fields} FROM {table} WHERE 
                                   {sign_column} = "{str(idq).replace('"', ggdfg)}"''').fetchone()
        else:
            debug_mess = f'''SELECT {fields} FROM {table} >>> '''
            data = bd.cursor().execute(f'''SELECT {fields} FROM {table}''').fetchall()
        if fields != "*" and len(fields.split(",")) == 1 and (not get_all):
            if data is None:
                debug(debug_mess + "None")
                return None
            debug(debug_mess + str(data[0]))
            return data[0]
        else:
            debug(debug_mess + str(data))
            return data
    except BaseException as e:
        debug("In", "getValueFromId", e)
        return False


async def write_value_from_id(idq, fields, value, table="users"):  # изменение значения в базе
    try:
        data = bd.cursor().execute(f"""UPDATE {table} SET {fields} = {value} WHERE id = {idq}""").fetchone()
        bd.commit()
        debug(f"""UPDATE {table} SET {fields} = {value} WHERE id = {idq}""")
        return data
    except BaseException as e:
        debug("In", "writeValueFromId", e)
        return False


async def add_user(idq):  # добавление пользователя в базу данных
    try:
        bd.cursor().execute("""INSERT INTO users (id) VALUES (?)""", (idq,))
        bd.commit()
    except sqlite3.Error as e:
        debug("Ошибка записи в БД:", e)
        return False
    debug("Добавлен новый пользователь, запись в БД завершена")
    return True


async def update_keyboard(message: types.Message):
    return types.ReplyKeyboardMarkup(keyboard=keyboards[global_variables.states[message.from_user.id]], resize_keyboard=True)


async def cut_into_messages(idq, separator, data):  # разрезаем текст на сообщения по id часов
    max_len = await get_value_from_id(idq, fields="maxLengthRussian", table="watches")
    lst = []
    while len(data) > max_len or separator in data:
        if separator in data[0:max_len]:
            ind = data[0:max_len].find(separator)
            lst.append(data[0:ind])
            data = data[ind + len(separator):]
        else:
            lst.append(data[0:max_len])
            data = data[max_len:]
    lst.append(data)
    return lst
