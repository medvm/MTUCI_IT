# -*- coding: utf-8 -*-
import telebot
from telebot import types
import functions, config

bot = telebot.TeleBot(config.token, parse_mode='MARKDOWN')

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = config.buttons['start_menu']
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Здравствуйте. Я подскажу расписание.', reply_markup=keyboard)

@bot.message_handler(commands=['week'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f'Сейчас {"чётная (нижняя)" if functions.odd_date_check() == 1 else "нечётная (верхняя)"} неделя')

@bot.message_handler(commands=['mtuci'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Cсылка на официальный сайт МТУСИ – https://mtuci.ru/')

@bot.message_handler(commands=['help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Краткая информацию о себе, краткая документация и список команд с их пояснениями: \
    \nосновная функция бота - ввод расписания \
    \n/start - начало работы: вывод приветствующего сообщения и клавиатуры с кнопками \
    \n/week - вывод текущей недели \
    \n/mtuci - вывод ссылки на официальный сайт МТУСИ \
    \n/help - вывод этого сообщения \
    \nна неверную команду бот отвечает сообщением "Извините, я Вас не понял" ')    
        
@bot.message_handler(content_types='text')
def message_reply(message):
    dataset = {'day': None, 'odd': None}
    dataset['odd'] = functions.odd_date_check()
    if message.text=="Расписание на текущую неделю":
        for day in range(5):
            bot.send_message(message.chat.id, functions.get_rasp(dataset['odd'], day))
    elif message.text=="Расписание на следующую неделю":
        for day in range(5):
            bot.send_message(message.chat.id, functions.get_rasp(not dataset['odd'], day))
    else:
        try:
            dataset['day'] = config.buttons['start_menu'].index(message.text)
            bot.send_message(message.chat.id, functions.get_rasp(dataset['odd'], dataset['day']))
        except:
            bot.send_message(message.chat.id, 'Извините, я Вас не понял')   

if __name__ == "__main__":
    bot.infinity_polling()
    