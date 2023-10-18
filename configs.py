from aiogram import types

CHOOSING_WATCH_TEXT = "Выбор браслета"
SETTINGS_TEXT = "Настройки"
BACK_TEXT = "Назад"

REVERSE_OR_STRAIGHT_SENDING_TEXT = "Отправка в прямом/обратном порядке"  # r           второй уровень настроек
SET_SEPARATOR_MESSAGES_TEXT = "Изменить разделитель"
SET_TIME_BETWEEN_MESSAGES_TEXT = "Изменить задержку между сообщениями"
SET_TIME_BEFORE_SENDING_TEXT = "Изменить время перед отправкой"
RESTART_THE_BOT_TEXT = "Отправить приветственное сообщение"

IN_PREPARING_TO_SENDING_STATE = -2
IN_SENDING_MESSAGES_STATE = -1
IN_SLEEP_STATE = 0  # sleep

IN_CHOICE_WATCH_STATE = 1  # in choice watch           второй уровень настроек
IN_SETTINGS_STATE = 2  # in settings

IN_SET_SEPARATOR_MESSAGES_STATE = 21  # 3                     третий уровень настроек
IN_SET_TIME_BETWEEN_MESSAGES_STATE = 22
IN_SET_TIME_BEFORE_SENDING_STATE = 23


SPLIT_BY_NEW_LINE_TEXT = "[Разбивать на сообщения по переводу строки]"
keyboards = {IN_SLEEP_STATE: [
    [
        types.KeyboardButton(text=CHOOSING_WATCH_TEXT),
        types.KeyboardButton(text=SETTINGS_TEXT),
    ], [
        types.KeyboardButton(text=RESTART_THE_BOT_TEXT),
    ]
], IN_SETTINGS_STATE: [
    [
        types.KeyboardButton(text=BACK_TEXT),
        types.KeyboardButton(text=REVERSE_OR_STRAIGHT_SENDING_TEXT),
    ], [
        types.KeyboardButton(text=SET_TIME_BETWEEN_MESSAGES_TEXT),
        types.KeyboardButton(text=SET_TIME_BEFORE_SENDING_TEXT),
    ], [
        types.KeyboardButton(text=SET_SEPARATOR_MESSAGES_TEXT),
    ]
], IN_SET_SEPARATOR_MESSAGES_STATE: [
    [
        types.KeyboardButton(text=BACK_TEXT),
    ], [
        types.KeyboardButton(text="[split]"),
        types.KeyboardButton(text="[s]"),
        types.KeyboardButton(text="..."),
        types.KeyboardButton(text=";;;"),
        types.KeyboardButton(text="==="),
        types.KeyboardButton(text=">>>"),
    ], [
        types.KeyboardButton(text=SPLIT_BY_NEW_LINE_TEXT),
    ]
], IN_SET_TIME_BEFORE_SENDING_STATE: [
    [
        types.KeyboardButton(text=BACK_TEXT),
    ], [
        types.KeyboardButton(text="2"),
        types.KeyboardButton(text="3"),
        types.KeyboardButton(text="4"),
        types.KeyboardButton(text="6"),
        types.KeyboardButton(text="10"),
        types.KeyboardButton(text="15"),
        types.KeyboardButton(text="30"),
    ],
], IN_SET_TIME_BETWEEN_MESSAGES_STATE: [
    [
        types.KeyboardButton(text=BACK_TEXT),
    ], [
        types.KeyboardButton(text="0.3"),
        types.KeyboardButton(text="0.5"),
        types.KeyboardButton(text="1"),
        types.KeyboardButton(text="2"),
        types.KeyboardButton(text="3"),
        types.KeyboardButton(text="5"),
        types.KeyboardButton(text="10"),
    ],
]
}

PROXY_URL = 'http://proxy.server:3128/'
ENABLE_DEBUG = True
TIMEZONE = 5
LENS_TEXT_BUTTONS = {1: 76, 2: 36, 3: 22, 4: 16, 5: 12, 6: 8}
MAX_QUANTITY_MESSAGES = 32
MAX_LEN_SEP = 16
MIN_TIME_BETWEEN_MESSAGES = 0.1
MAX_TIME_BETWEEN_MESSAGES = 16
MIN_TIME_BEFORE_MESSAGES = 2
MAX_TIME_BEFORE_MESSAGES = 32
TAG_FOR_SEPARATOR_START = "<sep>"
TAG_FOR_SEPARATOR_END = "</sep>"

DISCLAIMER = "⠀                       ДИС<b>КЛЕЙ</b>МЕР\n" \
             "Этот бот создан исключительно с целью тестирования большим количеством уведомлений за короткий " \
             "промежуток времени Ваших смарт-часов и фитнес-браслетов. Использование бота в иных целях не " \
             "предусмотрено.\n" \
             "Бездумное списывание без какого-либо изучения материала может плохо отразиться на успеваемости, " \
             "гораздо лучше писать бумажные шпаргалки самому. Автор данного бота не призывает им пользоваться и не " \
             "несёт ответственности за возможные последствия, всё, что Вы делаете, Вы делаете на свой страх и риск.\n"

HI_MES2 = '👋 Привет! Я бот для удобного списывания со смарт-часов, если что-то будет непонятно - можете спрашивать ' \
          'у автора (пока тут не слишком много пользователей), а также предлагать свои доработки. Контактов здесь ' \
          'нет по понятным причинам, но думаю Вы и так всё знаете.\n⠀                 ' \
          '<u>Краткая инструкция</u>\n' \
          '●Для принудительного разбиения текста на уведомления в конкретном месте - "[separator]". Предыдущее ' \
          'уведомление закончится перед "[separator]", а следующее начнётся после\n' \
          '●Изменить сочетание символов ' \
          'для разделителя, время отправки, выбранный браслет и другое, а также добавить новый браслет можно в ' \
          'настройках\n' \
          '●При отправке сообщения (сообщений) бот подождёт заданный промежуток времени и отправит ' \
          'полученный текст сообщениями нужной длины в этот чат. В приложении для браслета должны быть включены ' \
          'соответствующие уведомления\n' \
          '●Если Вам на часы приходят не все уведомления, попробуйте увеличить время ' \
          'между отправкой. Также возможно, что в памяти часов помещается меньшее количество сообщений, чем было ' \
          'отправлено\n' \
          '●Если в сообщении присутствует конструкция "' + TAG_FOR_SEPARATOR_START.replace("<", "&lt;") + '***' + \
          TAG_FOR_SEPARATOR_END.replace("<", "&lt;") + \
          '", то текст на месте *** будет использован в качестве разделителя при отправке данного сообщения\n' \
          '●Если вдруг что-то работает неправильно, попробуйте перезапустить бота командой /start\n\n' \
          'Для начала выберите свой браслет из меню выбора браслета:'

HI_LOGO = '''  ██████             ██████  ██░ ██ ▓█████ ▓█████▄▄██████▓  
▒▒████████         ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓█   ▀▓  ██▒ ▓▒  
▒▒██████████       ░ ▓██▄   ▒██▀▀██░▒███   ▒███  ▒ ▓██░ ▒░  
▒▒████    ████       ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒▓█  ▄░ ▓██▓ ░   
▒▒████      ████   ▒██████▒▒░▓█▒░██▓░▒████▒░▒████▒ ▒██▒ ░   
░░████        ████ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░░ ▒░ ░ ▒ ░░     
░░████████████████ ░ ░▒  ░ ░ ▒ ▒░░ ░ ░ ░  ░ ░ ░  ░   ░      
▒▒▓▓██      ▓▓████  ▄████▄ ░ ██░ ██ ▓█████ ▄▄▄░  ░ ▄▄██████▓
▒▒▓▓██      ▓▓████ ▒██▀ ▀█  ▓██░ ██▒▓█   ▀▒████▄ ░ ▓  ██▒ ▓▒
░░▒▒▒▒      ▓▓▒▒██ ▒▓█    ▄ ▒██▀▀██░▒███  ▒██  ▀█▄ ▒ ▓██░ ▒░
░░▒▒▒▒      ▓▓▒▒██ ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄░██▄▄▄▄██░ ▓██▓ ░ 
░░  ▒▒      ▒▒▒▒   ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▓█   ▓██▒ ▒██▒ ░ 
░░  ▒▒      ▒▒▒▒   ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░▒▒   ▓▒█░ ▒ ░░   
    ░░      ▒▒       ░  ▒    ▒ ░▒░ ░ ░ ░  ░ ▒   ▒▒ ░   ░    
    ░░      ▒▒     ░         ░  ░░ ░   ░    ░   ▒   /_)_ _/_
░░          ░░     ░ ░       ░  ░  ░   ░  ░     ░  /_)/_//  '''
