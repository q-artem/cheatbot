from bot import bd
import sqlite3


async def getValueFromId(idq, table="users", sign_column="id", fields="*"):  # получение значения из базы
    try:
        ggdfg = '""'
        print(f'''SELECT {fields} FROM {table} WHERE {sign_column} = "{str(idq).replace('"', ggdfg)}"''')
        data = bd.cursor().execute(f'''SELECT {fields} FROM {table} WHERE {sign_column} = "{str(idq).replace('"', ggdfg)}"''').fetchone()
        if fields != "*" and len(fields.split(",")) == 1:
            if data is None:
                return None
            return data[0]
        else:
            return data
    except BaseException as e:
        print("In", "getValueFromId", e)
        return False


async def writeValueFromId(idq, fields, value, table="users"):  # изменение значения в базе
    try:
        data = bd.cursor().execute(f"""UPDATE {table} SET {fields} = {value} WHERE id = {idq}""").fetchone()
        bd.commit()
        return data
    except BaseException as e:
        print("In", "writeValueFromId", e)
        return False


async def addUser(idq):  # добавление пользователя в базу данных
    try:
        bd.cursor().execute("""INSERT INTO users (id) VALUES (?)""", (idq,))
        bd.commit()
    except sqlite3.Error as e:
        print("Ошибка записи в БД")
        print(e)
        return False
    print("Добавлен новый пользователь, запись в БД завершена")
    return True


async def CutIntoMessages(idq, id_user, separator, data):  # разрезаем текст на сообщения по id часов и id юзера
    max_len = await getValueFromId(idq, fields="maxLengthRussian", table="watches")
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