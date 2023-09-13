import time
from asyncio import sleep

import telebot

from telebot import types

bot = telebot.TeleBot('6526631273:AAGSRuAdGfHE14VlDgRSz_ItXLnucj4S9gE')

separator = "[split]"

hiMess = '''                          ДИС*КЛЕЙ*МЕР
Этот бот создан исключительно с целью тестирования большим количеством уведомлений за короткий промежуток времени Ваших смарт-часов и фитнес-браслетов. Использование бота в иных целях не предусмотрено. Все совпадения случайны, как и нижеследующий текст. 

В общем, это мой бот для списывания с часов, в целом всё должно быть интуитивно понятно, но если нет, можете спрашивать у меня, а также предлагать свои доработки. Думаю, кто сделал бота Вы знаете.'''

@bot.message_handler(commands=['start'])
def start(message):

    #btn1 = types.KeyboardButton("👋 Поздороваться")
    #markup.add(btn1)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
    btn1 = types.KeyboardButton('xiaomi watсh 2 white')
    btn2 = types.KeyboardButton('Mi Band 7')
    btn3 = types.KeyboardButton('Amazfit gts 2 mini')
    btn4 = types.KeyboardButton('Моего браслета нет в списке')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, hiMess, reply_markup=markup, parse_mode='Markdown')
    bot.send_message(message.from_user.id, f"👋 Привет! Я твой бот-помощник! Чтобы выключить меня, напиши \"Здохни\"\nДля перезапуска - /start\nДля принудительного разбиения текста на уведомления в конкретном месте - {separator}\nВыбери свой браслет из меню:", reply_markup=markup)

maxLenNotification = dict()
allWatch = {180: 'xiaomi watсh 2 lite', 1023: 'Mi Band 7', 573: 'Amazfit gts 2 mini'}
lst = []        # проверено на русских   # проверено на русских    # проверено на русских
inputs = []

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.from_user.id)
    if message.text == "Здохни":
        bot.send_message(message.from_user.id, 'Неа, всё, отладка больше не работает', parse_mode='Markdown')
        return
    if message.text == "Здохни 31415926":
        bot.send_message(message.from_user.id, 'Okk', parse_mode='Markdown')
        bot.stop_polling()

    if message.from_user.id not in maxLenNotification.keys():
        maxLenNotification[message.from_user.id] = list(allWatch.keys())[0]

    for q in allWatch.items():
        if message.text == q[-1]:
            maxLenNotification[message.from_user.id] = q[0]
            bot.send_message(message.from_user.id, 'Принято', parse_mode='Markdown')
            return

    if message.text == 'Моего браслета нет в списке':
        bot.send_message(message.from_user.id, 'Ойй, не, ну а чего ты хотел, чтобы ещё и сторонние браслеты добавлять? Мне за это не платят', parse_mode='Markdown')
        return

    firstCall = False
    if inputs == []:
        firstCall = True

    inputs.append(message.text)

    if firstCall:
        print(maxLenNotification)
        bot.send_message(message.from_user.id, 'Принято, отправлю через 4 секунды c интервалом 3 секунды на браслет ' + allWatch[maxLenNotification[message.from_user.id]], parse_mode='Markdown')
        time.sleep(1.5) # пока задержка, досылаются сообщения
        print("Preparing to sending...")
        g = "".join(inputs)
        while len(g) > maxLenNotification[message.from_user.id] or separator in g:
            if separator in g[0:maxLenNotification[message.from_user.id]]:
                ind = g[0:maxLenNotification[message.from_user.id]].find(separator)
                lst.append(g[0:ind])
                g = g[ind + 7:]
            else:
                lst.append(g[0:maxLenNotification[message.from_user.id]])
                g = g[maxLenNotification[message.from_user.id]:]
        lst.append(g)
        while inputs != []:
            inputs.pop(0)

        while len(lst) > 0:
            if lst[0] == "":
                lst.pop(0)
                continue
            time.sleep(3)
            print("Sending", lst[0])
            bot.send_message(message.from_user.id, lst[0])
            lst.pop(0)
        print("Pass")
    else:
        bot.send_message(message.from_user.id, 'Добавлено ещё одно сообщение', parse_mode='Markdown')

if __name__ == '__main__':
    print("Starting bot...")
    bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть