# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import telebot 
import datetime
import threading
import time
import random
TOKEN='519695376:AAGgB9LqmRsiGPyYnDSWNCbMXxJqxRFBHas'
bot=telebot.TeleBot(TOKEN)

#@bot.message_handler(content_types=["text"])
#-226511191
url = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi"

def brous(day,weekDay):
	try:
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
		if len(schedule)>1:
			for i in range(len(schedule)-int(size)):
				numb.append(schedule[n])
				n=n+1
				time.append(schedule[n][0:5]+'-'+schedule[n][5:10])
				n=n+1
				things.append(schedule[n])
				n=n+1
			for i in range(int(a/3)):
				if things[i]=='':
					numb[i]=''
					time[i]=''
				else:	
					text=text+numb[i]+' пара ' +'('+time[i]+')'+'\n'+things[i]+'\n\n'
			text='Розклад на '+day+'('+weekDay+')'+'\n\n'+text	
		elif weekDay=='Saturday' or weekDay=='Sunday':
			text='Вихідний' 			
		else:
			text='Немає пар юху 👍'	
	except:
		text='Сайт з розкладом не працює'
	return text	



markup = telebot.types.ReplyKeyboardMarkup()
markup.row('⌛ Сьогодні', '⏳ Завтра')
markup.row('📅 День','📅 Тиждень')
markup.row('🕐 Дзвінки', '👽 Викладачі')
markup.row('Рулетка 🎰')
	
@bot.message_handler(commands=['start'])
def start(message):
	now= datetime.datetime.now()
	bot.send_message(message.chat.id,'А ось і розклад', reply_markup=markup)
	'''def clock(interval):
		while True:
			day=str(now.day)+'.'+str(now.month)+'.'+str(now.year)
			weekDay=datetime.datetime(now.year,now.month,now.day).strftime('%A')
			if now.hour==16:	
				bot.send_message(message.chat.id,brous(day,'Шухєєєєр розклад на завтра \n'+weekDay))  
			time.sleep(interval)  
	
	sec=60*60	
	t = threading.Thread(target=clock, args=(sec,))
	t.start()'''

@bot.message_handler(content_types=["text"])
def text(message):
	now= datetime.datetime.now()

	friends=['Васю','Влада','Кукляка','Липака','Пашкевичмана']
	rand=random.randrange(0,len(friends),1)
	dictt={'комп. мережі.':'Петришин Михайло Любомирович','моідо.':'Мазуренко Віктор Володимирович','педагогіка.':'Стинська Вікторія Володимирівна',
	'менеджмент.': 'Гречаник Наталія Юріївна','обробка зображ.':'Косаревич Ростислав Ярославович','комп. математика.':'Костишин Любов Павлівна',
	'паралельні. обчис.':'Горєлов Віталій Олевтинович','операційні. системи.':' Гейко Орест Ярославович'}
	scheduleDay={'Понеділок':'Monday','Вівторок':'Tuesday','Середа':'Wednesday','Четвер':'Thursday','Пятниця':'Friday'}
	#teacher 
	for i in dictt:
		if i in message.text.lower():
			bot.send_message(message.chat.id,dictt[i],reply_markup=markup)
	#day
	for i in scheduleDay:
		if i in message.text:
			nowDay=scheduleDay[i]
			dayNumb=now.day
			day=str(dayNumb)+'.'+str(now.month)+'.'+str(now.year)
			weekDay=datetime.datetime(now.year,now.month,dayNumb).strftime('%A')
			while True:
				if nowDay==weekDay:
					bot.send_message(message.chat.id,brous(day,weekDay),reply_markup=markup)
					break
				else:
					dayNumb+=1
					try:
						day=str(dayNumb)+'.'+str(now.month)+'.'+str(now.year)
						weekDay=datetime.datetime(now.year,now.month,dayNumb).strftime('%A')	
					except:
						weekDay=datetime.datetime(now.year,now.month+1,1).strftime('%A')
						day=str(dayNumb)+'.'+str(now.month+1)+'.'+str(now.year)	
				
	
	if message.text=='⌛ Сьогодні':
		day=str(now.day)+'.'+str(now.month)+'.'+str(now.year)
		weekDay=datetime.datetime(now.year,now.month,now.day).strftime('%A')
		bot.send_message(message.chat.id,brous(day,weekDay))
	#schedule 		
	if message.text=='🕐 Дзвінки':
		schedule='1 пара 9:00-10:20 \n 2 пара 10:30-11:50 \n 3 пара 12:15-13:35 \n 4 пара 13:50-15:10 \n 5 пара 15:25-16:45 \n 6 пара 16:55-18:15'
		bot.send_message(message.chat.id,schedule)			
	#Tomorrow schedule 
	if message.text=='⏳ Завтра':
		try:
				day=str(now.day+1)+'.'+str(now.month)+'.'+str(now.year)
				weekDay=datetime.datetime(now.year,now.month,now.day+1).strftime('%A')
		except:
				weekDay=datetime.datetime(now.year,now.month+1,1).strftime('%A')
				day=str(1)+'.'+str(now.month+1)+'.'+str(now.year)
		bot.send_message(message.chat.id,brous(day,weekDay))
	#Friends roulette
	if message.text=='Рулетка 🎰':
		bot.send_message(message.chat.id,'Рандом вибрав підаром '+ friends[rand])	
	if message.text=='👽 Викладачі':
		teach = telebot.types.ReplyKeyboardMarkup()
		teach.row('МОІДО.', 'Операційні. системи.')
		teach.row('Педагогіка.', 'Менеджмент.')
		teach.row('Комп. Математика.', 'Комп. Мережі.')
		teach.row('Паралельні. обчис.', 'Обробка зображ.')
	
		bot.send_message(message.chat.id,'Виберіть предмет з якого хочете знати викладача',reply_markup=teach)	

	if message.text=='📅 День':
		days = telebot.types.ReplyKeyboardMarkup()
		days.row('Понеділок')
		days.row('Вівторок')
		days.row('Середа')
		days.row('Четвер')
		days.row('Пятниця')
		bot.send_message(message.chat.id,'Виберіть день',reply_markup=days)	


	if message.text=='📅 Тиждень':
		n=0
		dayNumb=now.day
		
		while True:
			day=str(dayNumb)+'.'+str(now.month)+'.'+str(now.year)
			weekDay=datetime.datetime(now.year,now.month,dayNumb).strftime('%A')
			if weekDay=='Saturday' or weekDay=='Sunday':
				dayNumb+=1
			else:	
				n+=1
				bot.send_message(message.chat.id,brous(day,weekDay))
				dayNumb+=1
				try:
					weekDay=datetime.datetime(now.year,now.month,dayNumb).strftime('%A')
				except:
					weekDay=datetime.datetime(now.year,now.month+1,1).strftime('%A')	
				day=str(dayNumb)+'.'+str(now.month)+'.'+str(now.year)
				if n==5:
					break
			
bot.polling()    