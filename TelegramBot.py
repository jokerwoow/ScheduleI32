# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import telebot 
import datetime
from time import sleep
TOKEN='519695376:AAGgB9LqmRsiGPyYnDSWNCbMXxJqxRFBHas'
bot=telebot.TeleBot(TOKEN)

#@bot.message_handler(content_types=["text"])
#-226511191
url = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi"
def brous(day,weekDay):
	response = requests.post(url,data={'group':'ІНФ-32'.encode('cp1251'),'sdate':day,'btn btn-success':'true','faculty':'1002'})
	text=str(response.text.encode('iso-8859-1').decode('cp1251'))
	soup = BeautifulSoup(text,'html.parser')
	
	schedule=[] 
	time=[]
	numb=[]
	things=[]
	
	text=''

	divTag = soup.find("div", {"class": "container"})
	
	for tag in divTag:
	    tdTags = tag.find_all("td")
	    for tag in tdTags:
	        schedule.append(tag.text)   
	a=len(schedule)        
	size=a-(a/3)
	n=0
	if len(schedule)>1 and weekDay<=4:
		for i in range(len(schedule)-int(size)):
			numb.append(schedule[n])
			n=n+1
			time.append(schedule[n][0:5]+'-'+schedule[n][5:10])
			n=n+1
			things.append(schedule[n])
			n=n+1
		for i in range(int(a/3)):
			text=text+numb[i]+' пара ' +'('+time[i]+')'+'\n'+things[i]+'\n'
		text='Розклад на '+day+'('+datetime.datetime.now().strftime('%A')+')'+'\n'+text	
	elif weekDay>4:	
		text='Завтра вихідні хулі'		
	else:
		text='Завтра немає пар юху 	👍\n Або сайт з розкладом накрився 👎'	
	return text	
def botMessage(text):	
	bot.send_message(355875782,text)

'''while True:	
	now= datetime.datetime.now()
	day=str(now.day+1)+'.'+str(now.month)+'.'+str(now.year)
	hour=now.hour
	if hour==17:
		botMessage(brous(day))	
	sleep(3600)	'''
@bot.message_handler(commands=['td'])
def today(message):
	now= datetime.datetime.now()
	day=str(now.day)+'.'+str(now.month)+'.'+str(now.year)
	weekDay=now.weekday()
	bot.send_message(355875782,brous(day,weekDay))	

@bot.message_handler(commands=['tm'])
def tommorrow(message):
	now= datetime.datetime.now()
	day=str(now.day+1)+'.'+str(now.month)+'.'+str(now.year)
	weekDay=now.weekday()+1
	bot.send_message(355875782,brous(day,weekDay))	
@bot.message_handler(commands = ['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='https://habrahabr.ru')
    markup.add(btn_my_site)
    bot.send_message(355875782, "Нажми на кнопку и перейди на наш сайт.", reply_markup = markup)
bot.polling()    