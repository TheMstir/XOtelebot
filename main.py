import telebot
import random
import time

from telebot import types
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

import config

# это у нас местная 'база данных для пользователя' пока что в ней храниться только список,
# но зато под каждого пользователя
cash_storage = StateMemoryStorage()

# основной элемент для связки
bot = telebot.TeleBot(config.ticket, state_storage=cash_storage)


class MyStates(StatesGroup):
    """Хранлилище для промежуточных данных игры"""
    zone = State()  # для хранения игрового пространства
    win_flag = State() #

    name = State() # для доски почета
    count_win = State() # подсчет побед. поражения это все минус победы
    count_game = State() # общее количество сыгранных игр
    precent_difficult = State() # если придумаю сложность


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    """
        Меню навигации в виде записи для помощи
        позволяет пользователю разобраться и быстро
        пользоваться особенностями простенькой программы
        """

    rand_m = random.randint(1, 2)

    mess = f'Привет! <b>{message.from_user.first_name}</b> '

    bot.send_message(message.chat.id, mess, parse_mode='HTML')
    mess = '''Привет я ❌⭕ бот! Хочешь поиграть в крестики-нолики?:
/start Чтобы перезапустить это меню
/lets_go 🎯 Запустит игру! 
    
/legends Будет показывать лучший счет и историю ходов в нем
/cancel ❌ Отменяет введенные данные и позволяет сразу начать сначала
        '''

    bot.send_message(message.chat.id, mess, parse_mode='HTML')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👋 Начинаем играть!", "❓ Help/Menu")
    bot.send_message(message.from_user.id, 'Я умею не так уж и много, но тут уж куда деваться, '
                                           'я создан только чтобы играть с тобой в крестики и нолики',
                     reply_markup=markup)


@bot.message_handler(commands=['lets_go'])
def base_game_func(message: types.Message):

    bot.set_state(message.from_user.id, MyStates.zone, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['zone'] = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    mess = ' '.join(data['zone'])
    bot.send_message(message.chat.id, mess, parse_mode='HTML')

    letsplay(message, data)


def letsplay(message, data):
    #while True:
        # рисуется сетка кнопок
        # if нет флага победы
    in_action(message, data['zone'])
        # elif


def in_action(message, base):
    markup_inline = types.InlineKeyboardMarkup()
    item_first = types.InlineKeyboardButton(text=base[0], callback_data='1')
    item_second = types.InlineKeyboardButton(text=base[1], callback_data='2')
    item_third = types.InlineKeyboardButton(text=base[2], callback_data='3')
    item_four = types.InlineKeyboardButton(text=base[3], callback_data='4')
    item_five = types.InlineKeyboardButton(text=base[4], callback_data='5')
    item_six = types.InlineKeyboardButton(text=base[5], callback_data='6')
    item_seven = types.InlineKeyboardButton(text=base[6], callback_data='7')
    item_eight = types.InlineKeyboardButton(text=base[7], callback_data='8')
    item_nine = types.InlineKeyboardButton(text=base[8], callback_data='9')

    markup_inline.add(item_first, item_second, item_third, item_four, item_five, item_six, item_seven, item_eight, item_nine)
    bot.send_message(message.chat.id, f'Отлично, ваш ход',
                     reply_markup=markup_inline)

    # bot.set_state(message.from_user.id, MyStates.zone, message.chat.id)
    # data = cash_storage.get_data(message.from_user.id, message.chat.id)


def resort(message, base):
    print(base)
    markup_inline = types.InlineKeyboardMarkup()
    item_first = types.InlineKeyboardButton(text=base['zone'][0], callback_data='/lets_go')
    item_second = types.InlineKeyboardButton(text=base['zone'][1], callback_data='/lets_go')
    item_third = types.InlineKeyboardButton(text=base['zone'][2], callback_data='/lets_go')
    item_four = types.InlineKeyboardButton(text=base['zone'][3], callback_data='/lets_go')
    item_five = types.InlineKeyboardButton(text=base['zone'][4], callback_data='/lets_go')
    item_six = types.InlineKeyboardButton(text=base['zone'][5], callback_data='/lets_go')
    item_seven = types.InlineKeyboardButton(text=base['zone'][6], callback_data='/lets_go')
    item_eight = types.InlineKeyboardButton(text=base['zone'][7], callback_data='/lets_go')
    item_nine = types.InlineKeyboardButton(text=base['zone'][8], callback_data='/lets_go')

    markup_inline.add(item_first, item_second, item_third, item_four, item_five, item_six, item_seven,
                      item_eight, item_nine)
    bot.send_message(message.chat.id, f'Вы победили!', reply_markup=markup_inline)
    bot.send_message(message.chat.id, 'Начнем заново? /lets_go')


@bot.callback_query_handler(func=lambda call: True)
def callbacker(call: types.CallbackQuery):
    """
    тэйкбэйкер
    управление кнопками
    """
    place = 0
    if call.data == '1':
        place = 0
    elif call.data == '2':
        place = 1
    elif call.data == '3':
        place = 2
    elif call.data == '4':
        place = 3
    elif call.data == '5':
        place = 4
    elif call.data == '6':
        place = 5
    elif call.data == '7':
        place = 6
    elif call.data == '8':
        place = 7
    elif call.data == '9':
        place = 8

    bot.set_state(call.from_user.id, MyStates.zone, call.message.chat.id)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        while True:
            if data['zone'][place] != '❌' and data['zone'][place] != '⭕':
                data['zone'][place] = '❌'
                break
            else:
                in_action(call.message, data)

        # ход противника базово
        while True:
            dice = random.randint(0, 8)
            if data['zone'][dice] != '❌' and data['zone'][dice] != '⭕':
                data['zone'][dice] = '⭕'
                break
            else:
                dice = random.randint(0, 8)

    bord = ''
    for i in data['zone']:
        for j in i:
            bord += j
    print(bord)

    if bord[0:3] == '❌' * 3 or bord[3:6] == '❌' * 3 or bord[6:] == '❌' * 3 or bord[0::4] == '❌' * 3 or \
            bord[2:7:2] == '❌' * 3 or bord[0:8:3] == '❌' * 3 or bord[1:9:3] == '❌' * 3 or bord[2::3] == '❌' * 3:
        resort(call.message, data)
        # отсюда возвращается победа.

    elif '1' not in bord and '2' not in bord and '3' not in bord and '4' not in bord and '5' not in bord \
            and '6' not in bord and '7' not in bord and '8' not in bord and '9' not in bord:
        bot.send_message(call.message.chat.id, 'Ничья! Начнем заново? /start', parse_mode='HTML')
        time.sleep(0.5)

    else:
        letsplay(call.message, data)


def incorrect(message: types.Message) -> None:
    """
    При каком-либо неправильном вводе должно направлять сюда
    """
    bot.send_message(message.chat.id, 'Случилось что-то непонятное... я еще в разработке... '
                                      'да даже я могу быть в разработке отправляю вас в начало')
    base_game_func(message)


@bot.message_handler(state="*", commands=['cancel'])
def any_state(message: types.Message) -> None:
    """
    Сброс данных в States по запросу пользователя
    """
    data = cash_storage.get_data(message.from_user.id, message.chat.id)
    # 'очищает' поле
    data['zone'] = ['1','2','3','4','5','6','7','8','9']

    bot.send_message(message.chat.id, "Начнем сначала!")

    # запускает игру сначала
    base_game_func(message)


@bot.message_handler(content_types=['text'])
def date_from_user(message: types.Message) -> None:
    """
    Базовый механизм меню, позволяет переноситься по функционалу доступными кнопками
    """
    if message.text == '👋 Начинаем играть!':
        base_game_func(message)
    if message.text == '❓ Help/Menu':
        send_welcome(message)



bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)