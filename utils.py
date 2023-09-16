from bot import bd
import sqlite3
from configs import ENABLE_DEBUG


def debug(*args, sep=' ', end='\n', file=None):
    if ENABLE_DEBUG:
        print("->", *args, sep=sep, end=end, file=file)
        return True
    else:
        return False


async def get_value_from_id(idq, table="users", sign_column="id", fields="*"):  # получение значения из базы
    try:
        ggdfg = '""'
        debug(f'''SELECT {fields} FROM {table} WHERE {sign_column} = "{str(idq).replace('"', ggdfg)}"''')
        data = bd.cursor().execute(f'''SELECT {fields} FROM {table} WHERE 
                                   {sign_column} = "{str(idq).replace('"', ggdfg)}"''').fetchone()
        if fields != "*" and len(fields.split(",")) == 1:
            if data is None:
                return None
            return data[0]
        else:
            return data
    except BaseException as e:
        debug("In", "getValueFromId", e)
        return False


async def write_value_from_id(idq, fields, value, table="users"):  # изменение значения в базе
    try:
        data = bd.cursor().execute(f"""UPDATE {table} SET {fields} = {value} WHERE id = {idq}""").fetchone()
        bd.commit()
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
