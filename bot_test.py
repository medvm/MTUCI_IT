import telebot
token='2116215044:AAH0qbYOn1eO_me5jJ4uNrhGDnH5fYR5rkU'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Do you wanna know about MTUCI?")
	keyboard = types.ReplyKeyboardMarkup(True,False)
    keyboard.row('yeah','no thx')
    send = bot.send_message(message.chat.id, reply_markup=keyboard)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def answer(message):
	if message.text.lower() == 'yeah':
		bot.send_message(message.chat.id, "Chek this out: https://mtuci.ru")
	elif message.text.lower() == 'no, thx':
		bot.send_message(message.chat.id, "Go fuck yourself")
	

bot.infinity_polling()