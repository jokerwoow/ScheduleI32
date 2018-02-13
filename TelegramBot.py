# -*- coding: utf-8 -*-
import telebot 
import datetime
import brouser
TOKEN='519695376:AAGgB9LqmRsiGPyYnDSWNCbMXxJqxRFBHas'
bot=telebot.TeleBot(TOKEN)

#@bot.message_handler(content_types=["text"])
@bot.message_handler(commands=['start'])
def start(message):
		sent=bot.send_message(355875782,brouser.text)

'''if __name__ =='__main__':	
	bot.polling(none_stop=True)		'''
bot.polling()	