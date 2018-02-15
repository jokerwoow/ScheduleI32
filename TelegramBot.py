# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import telebot 
import datetime
from time import sleep
TOKEN='519695376:AAGgB9LqmRsiGPyYnDSWNCbMXxJqxRFBHas'
bot=telebot.TeleBot(TOKEN)

#@bot.message_handler(content_types=["text"])


now = datetime.datetime.now()
today=str(now.day+1)+'.'+str(now.month)+'.'+str(now.year)
url = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi"
def brous():
	response = requests.post(url,data={'group':'ІНФ-32'.encode('cp1251'),'sdate':today,'btn btn-success':'true','faculty':'1002'})
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
			text=text+numb[i]+' пара ' +'('+time[i]+')'+'\n'+things[i]+'\n'	
	else:
		text='Завтра немає пар юху 	👍\n Або сайт накрився 👎'	
	return text	
def botMessage(text):	
	bot.send_message(355875782,text)
while True:	
	yep= datetime.datetime.now()
	hour=yep.hour
	if hour==22:
		botMessage(brous())		
	sleep(3600)	