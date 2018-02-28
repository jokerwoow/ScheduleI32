# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import telebot 
import datetime
from time import sleep
import random
TOKEN='519695376:AAGgB9LqmRsiGPyYnDSWNCbMXxJqxRFBHas'
bot=telebot.TeleBot(TOKEN)

#@bot.message_handler(content_types=["text"])
#-226511191
url = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi"

def brous(day,weekDay,tmTd):
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
					text=''
				else:	
					text=text+numb[i]+' пара ' +'('+time[i]+')'+'\n'+things[i]+'\n\n'
			text='Розклад на '+day+'('+weekDay+')'+'\n\n'+text	
		elif weekDay=='Saturday' or weekDay=='Sunday':
			text=tmTd+'Вихідний' 			
		else:
			text=tmTd+'немає пар юху 👍'	
	except:
		text='Сайт з розкладом не працює'
	return text	
	'''elif weekDay>4:	
		text='Вихідниииииий'''
#Автовідправка 
'''def botMessage(text):	
	bot.send_message(-226511191,text)

while True:	
	now= datetime.datetime.now()
	day=str(now.day+1)+'.'+str(now.month)+'.'+str(now.year)
	hour=now.hour
	if hour==17:
		botMessage(brous(day))	
	sleep(3600)	'''
markup = telebot.types.ReplyKeyboardMarkup()
markup.row('/Сьогодні', '/Завтра')
markup.row('/Розклад', '/Викладач')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'А ось і розклад', reply_markup=markup)

@bot.message_handler(commands=['Сьогодні'])
def today(message):
	now= datetime.datetime.now()
	day=str(now.day)+'.'+str(now.month)+'.'+str(now.year)
	weekDay=datetime.datetime(now.year,now.month,now.day).strftime('%A')
	tmTd='Сьогодні '
	bot.send_message(message.chat.id,brous(day,weekDay,tmTd))	

@bot.message_handler(commands=['Завтра'])
def tommorrow(message):
	now = datetime.datetime.now()
	
	try:
		day=str(now.day+1)+'.'+str(now.month)+'.'+str(now.year)
		weekDay=datetime.datetime(now.year,now.month,now.day+1).strftime('%A')
	except:
		weekDay=datetime.datetime(now.year,now.month+1,1).strftime('%A')
		day=str(1)+'.'+str(now.month+1)+'.'+str(now.year)	
	tmTd='Завтра '
	bot.send_message(message.chat.id,brous(day,weekDay,tmTd))
@bot.message_handler(commands=['Викладач'])
def teacher(message):
	teach = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
	teach.row('МОІДО.', 'Операційні. системи.')
	teach.row('Педагогіка.', 'Менеджмент.')
	teach.row('Комп. Математика.', 'Комп. Мережі.')
	teach.row('Паралельні. обчис.', 'Обробка зображ.')

	bot.send_message(message.chat.id,'Виберіть предмет з якого хочете знати викладача',reply_markup=teach)

@bot.message_handler(commands=['Розклад'])
def time(message):
	schedule='1 пара 9:00-10:20 \n 2 пара 10:30-11:50 \n 3 пара 12:15-13:35 \n 4 пара 13:50-15:10 \n 5 пара 15:25-16:45 \n 6 пара 16:55-18:15'
	bot.send_message(message.chat.id,schedule)	
@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id,'/td-розклад на сьогодні\n/tm-розклад на завтра\n/time-розклад пар\n/help-догадаєтесь самі👍')	

@bot.message_handler(content_types=["text"])
def text(message):
	now= datetime.datetime.now()
	lox=['Лашара я тебе хейчу','Пздц ти лох','Льоха підр','Боже льоха чого ти такий мудак?',
	'Ой та закрийся вже','Всьо тобі пизда','Тікай з села мудак по тебе виїхали']

	today=['які пари сьогодні','які пари','які сьогодні пари']

	tomorrow=['які пари завтра','які завтра пари','які в нас пари завтра','які пари взагалі завтра']

	dictt={'комп. мережі.':'Петришин Михайло Любомирович','моідо':'Мазуренко Віктор Володимирович','педагогіка.':'Стинська Вікторія Володимирівна',
	'менеджмент.': 'Гречаник Наталія Юріївна','обробка зображ.':'Косаревич Ростислав Ярославович','комп. математика.':'Костишин Любов Павлівна',
	'паралельні. обчис.':'Горєлов Віталій Олевтинович','операційні. системи.':' Гейко Орест Ярославович'}
	oleksiy=random.randrange(0,len(lox))
	
	for i in today:
		if message.text.lower()==i:
			day=str(now.day)+'.'+str(now.month)+'.'+str(now.year)
			weekDay=datetime.datetime(now.year,now.month,now.day).strftime('%A')
			bot.send_message(message.chat.id,message.from_user.first_name+' '+message.from_user.last_name +'\n'+brous(day,weekDay,'Сьогодні '))
	for j in tomorrow:
		if message.text.lower()==j:
			day=str(now.day+1)+'.'+str(now.month)+'.'+str(now.year)
			weekDay=datetime.datetime(now.year,now.month,now.day+1).strftime('%A')
			bot.send_message(message.chat.id,message.from_user.first_name+' '+message.from_user.last_name +'\n'+brous(day,weekDay,'Завтра '))
	for i in dictt:
		if i in message.text.lower():
			bot.send_message(message.chat.id,dictt[i])
			bot.send_message(message.chat.id,'тадам',reply_markup=markup)
	if message.from_user.first_name=='Oleksii' and message.from_user.last_name=='Pashkevych':
		bot.send_message(message.chat.id,lox[oleksiy]) 		
bot.polling()    