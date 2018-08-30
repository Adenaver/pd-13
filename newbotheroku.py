from bs4 import BeautifulSoup
import requests
import datetime
import telebot
import re
import time
import os
import random
import shelve
import psycopg2
from flask import Flask, request
from top import top_test
from random import choice
from string import ascii_uppercase
from update_score import new_score
from update_time import new_time
TOKEN = os.environ.get('TOKEN')
hostname = os.environ.get('hosting')
username = os.environ.get('user')
password = os.environ.get('password')
database = os.environ.get('bdname')
unaviable = u'\U0001F512' # unaviable
success = u'\U00002705' # unaviable
close = u'\U0000274C' # unaviable
sby= u'\U0001F4E1' # sby text 1F4DD
rashif = u'\U0001F4DD' # расшифровка сбу
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
schedule_markup = telebot.types.ReplyKeyboardMarkup(True, False)
schedule_markup.row('Сегодня', 'Завтра')
hide = telebot.types.ReplyKeyboardRemove()
keyboard = telebot.types.InlineKeyboardMarkup()
call1 = telebot.types.InlineKeyboardButton(text="Cегодня", callback_data="today")
call2 = telebot.types.InlineKeyboardButton(text="Завтра", callback_data="nextday")
keyboard.add(call1,call2)
hide = telebot.types.ReplyKeyboardRemove()
def log(message,answer):
    print("\n-----")
    from datetime import datetime
    print(datetime.now())
    print("Сообещние от {0} {1} (id={2})\nТекст: {3}".format(message.from_user.first_name,
                                                                message.from_user.last_name,
                                                                str(message.from_user.id),
                                                                message.text))
    print("Ответ:",answer)
today = datetime.datetime.now()
group_data = '1261'
def parsing_timetable(week,date_one):
    #bot.send_message(call.message.chat.id, "🚫 Летом данная функция не доступна.")
    nontification(message,3)
    today = datetime.datetime.now()
    #date_one= today.strftime("%d.%m.%Y")
    #date_two = today.strftime("%d.%m.%Y")
    #date_one="03.09.2018"
    #date_two="07.09.2018"
    schedule_url='http://e-rozklad.dut.edu.ua/timeTable/group?TimeTableForm%5Bfaculty%5D=1&TimeTableForm%5Bcourse%5D=1&TimeTableForm%5Bgroup%5D=1261&TimeTableForm%5Bdate1%5D={}&TimeTableForm%5Bdate2%5D={}&TimeTableForm%5Br11%5D=5&timeTable=0'.format(date_one,date_one)
    for i in range(1):
        page = requests.post(schedule_url, data=group_data)
        soup = BeautifulSoup(page.text, 'html.parser')

        schedule_table = soup.find("table", {"id": "timeTableGroup"})

        header_list = [div.text for div in soup.find_all('option', selected=True)]
        print(header_list)
        lessons_data = [div.text.replace('\r', '').replace('\n', '').replace('    ', ' ')[:-1]
                        for div in schedule_table.findAll('div', attrs={"class": "cell mh-50"})][:-2]

        lessons_date = [i.text for i in schedule_table.findAll('div') if len(i.get_text()) == 10][:-2]
        print(lessons_date)
        lessons_order = [str(div.text[:2]) for div in schedule_table.findAll('div',
                                        attrs={"class": "mh-50 cell cell-vertical"})][:-2]
        print(lessons_order)

        lessons_count = [div.text.count('пара') for div in schedule_table.findAll('td') if 'пара' in div.text][:-2]
        data, order = [], []
        print(lessons_date[4])
        #print(lessons_count)
        for count in lessons_count:
            data.append(lessons_data[:count])
            order.append([int(point) for point in lessons_order[:count]])

            lessons_data = lessons_data[count:]
            lessons_order = lessons_order[count:]
        print(order)
        print(week)
        for day, k in zip(data, order):
            store = {}
            for i in range(len(day)):
                if len(day[i]) is not 0:
                    store['lesson_order'] = order[week][i]
                    store['lesson_title'] = day[i][:day[i].index('ауд')-1]
                    day[i] = day[i][day[i].index('ауд'):]
                    store['lesson_classroom'] = ' '.join(day[i].split()[:2])
                    store['lesson_teacher'] = ' '.join(day[i].split()[2:])
                    day[i] = store
                    store = {}
        if week ==5 or week ==6:
            bot.send_message(call.message.chat.id,"Сегодня пар нету.")
        for day, k in zip(data, order):
            store = {}
            for i in range(len(day)):
                if len(day[i]) is not 0:
                    store = day[i]
                    bot.send_message(call.message.chat.id,str(store['lesson_order']) +' пара\n|' + str(store['lesson_title']) +' | '+ str(store['lesson_classroom']) +'\n - '+ str(store['lesson_teacher']))
                    print(store['lesson_order'])
                    print(store['lesson_title'])
                    print(store['lesson_classroom'])
                    print(store['lesson_teacher'])
                    store = {}
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        today= datetime.datetime.now()
        if call.data == "today":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Проверяем...")
            date_one=today.strftime("%d.%m.%Y")
            week= today.weekday()
            parsing_timetable(week,date_one)
        if call.data == "nextday":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Проверяем...")
            date_two = today+datetime.timedelta(days=1)
            week= date_two.weekday()
            date_two=date_two.strftime("%d.%m.%Y")
            parsing_timetable(week,date_two)
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Ошибка")
def nontification(message,type):
    first = message.from_user.first_name
    last = message.from_user.last_name
    now=datetime.datetime.now()
    if type == 1:
        bot.send_message(376995776,"Внимание: попытка регистрации,активации,удаления.\nИмя: "+str(first)+" "+str(last)+" \nUserID: "+str(message.from_user.id)+"\nВремя: "+str(now))
    elif type == 2:
        bot.send_message(376995776,"Внимание: запущенна рулетка.\nИмя: "+str(first)+" "+str(last)+" \nUserID: "+str(message.from_user.id)+"\nВремя: "+str(now))
    elif type == 3:
        bot.send_message(376995776,"Внимание: запрос на расписание.\nИмя: "+str(first)+" "+str(last)+" \nUserID: "+str(message.from_user.id)+"\nВремя: "+str(now))
    else:
        bot.send_message(376995776,"Внимание: не индефицировананный запрос к боту.\nИмя: "+str(first)+" "+str(last)+" \nUserID: "+str(message.from_user.id)+"\nВремя: "+str(now))
@bot.message_handler(commands=['menu'])
def ss(message):
    bot.send_message(message.chat.id,"Доступные действия:",reply_markup=keyboard)
@bot.message_handler(commands=['top'])
def top_lst(message):
    top_test(message)
@bot.message_handler(commands=['remove'])
def nulled(message):
    if message.from_user.id== 376995776:
        remove()
    else:
        bot.send_message(message.chat.id,"🔒 У тебя нет прав на эту команду.")
        print(mes)
@bot.message_handler(commands=['reg'])
def status(message):

@bot.message_handler(commands=['my_wins'])
def check_user(message):
    if message.from_user.id == 312023065 or message.from_user.id == 345694869 or message.from_user.id == 650340191 or message.from_user.id == 650340191 or message.from_user.id == 482906929 or message.from_user.id == 290522978 or message.from_user.id == 559066333:
        bot.send_message(message.chat.id,"Ваша учетная запись заблокированна.",)
        nontification(message)
    else:
        con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        cur = con.cursor()
        id=message.from_user.id
        try:
            cur.execute("SELECT id FROM users WHERE user_id = %s",(id,))
            row=cur.fetchone()
            wins=row[0]
            bot.send_message(message.chat.id,"У тебя - "+str(wins)+" побед.")
        except TypeError:
            bot.send_message(message.chat.id,"В базе не найдена ваша запись.")
        con.close()
#@bot.message_handler(commands=['check_users'])
#def check_user(message):
#    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
#    cur = con.cursor()
#    cur.execute("SELECT * FROM users")
#    while True:
#        row = cur.fetchone()
#        if row == None:
#            break
#        elif row[3]==None:
#            bot.send_message(message.chat.id,"🚨 У пользователя "+str(row[2])+" не заполненно поле Фамилия.")
#    con.commit()
#    con.close()
@bot.message_handler(commands=['spin'])
def prespin(message):
    if message.from_user.id == 312023065 or message.from_user.id == 345694869 or message.from_user.id == 650340191 or message.from_user.id == 650340191 or message.from_user.id == 482906929 or message.from_user.id == 290522978 or message.from_user.id == 559066333:
        bot.send_message(message.chat.id,"Ваша учетная запись заблокированна.",)
        nontification(message,1)
    else:
        bot.send_message(message.chat.id,"Лоторея закрыта.",)
def spin(message):
    today = datetime.datetime.now()
    now=today.strftime('%d%m')
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("SELECT last_time FROM times WHERE user_id = 123")
    row=cur.fetchone()
    info_bd=row[0]
    con.close()
    if info_bd!=now:
        rand=random.randint(1,3)
        if rand==1:
            counter=0
            con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                else:
                    print(str(row[2])+str(row[3]))
                    counter+=1
            print("Кол-во участников: "+str(counter))
            con.commit()
            con.close()
            bot.send_message(message.chat.id,sby+" Поиск по базам СБУ...")
            time.sleep(5)
            bot.send_message(message.chat.id,rashif+" Расшифровываем информацию...")
            time.sleep(5)
            randomizer=random.randint(0,counter-1)
            print("Выбран рандомно: "+str(randomizer))
            con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = con.cursor()
            winner="null"
            cur.execute("SELECT * FROM users")
            for i in range(counter):
                row = cur.fetchone()
                if row == None:
                    print("Остановка поиска. Конец БД")
                    break
                elif i==randomizer:
                    if row[2]=="null":
                        bot.send_message(message.chat.id,"Сегодня красавчик дня: "+str(row[2])+" "+" 👑")
                    else:
                        bot.send_message(message.chat.id,"Сегодня красавчик дня: "+str(row[2])+" "+str(row[3])+" 👑")
                    winner=str(row[2])+" "+str(row[3])
                    id=row[1]
                    new_score(id)
                print("Ход поиска:"+str(i))
            last= datetime.datetime.now()
            times=last.strftime('%d%m')
            new_time(times,winner)
            con.commit()
            con.close()
        if rand==2:
            counter=0
            con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                else:
                    counter+=1
            print("Кол-во участников: "+str(counter))
            con.commit()
            con.close()
            bot.send_message(message.chat.id,"☕ Гадаем на кофейной гуще...")
            time.sleep(5)
            bot.send_message(message.chat.id,"🌟 Смотрим на звезды...")
            time.sleep(5)
            randomizer=random.randint(0,counter-1)
            print("Выбран рандомно: "+str(randomizer))
            con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            for i in range(counter):
                row = cur.fetchone()
                if row == None:
                    print("Остановка поиска. Конец БД")
                    break
                elif i==randomizer:
                    if row[2]=="null":
                        bot.send_message(message.chat.id,"Сегодня красавчик дня: "+str(row[2])+" "+" 👑")
                    else:
                        bot.send_message(message.chat.id,"Сегодня красавчик дня: "+str(row[2])+" "+str(row[3])+" 👑")
                    winner=str(row[2])+" "+str(row[3])
                    id=row[1]
                    new_score(id)

                print("Ход поиска:"+str(i))
            last= datetime.datetime.now()
            times=last.strftime('%d%m')
            new_time(times,winner)
            con.commit()
            con.close()
        if rand==3:
            counter=0
            con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                else:
                    counter+=1
            print("Кол-во участников: "+str(counter))
            con.commit()
            con.close()
            bot.send_message(message.chat.id,"🃏 Раскладываем карты...")
            time.sleep(5)
            bot.send_message(message.chat.id,"🔮 Спрашиваем у духов...")
            time.sleep(5)
            randomizer=random.randint(0,counter-1)
            print("Выбран рандомно: "+str(randomizer))
            con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            for i in range(counter):
                row = cur.fetchone()
                if row == None:
                    print("Остановка поиска. Конец БД")
                    break
                elif i==randomizer:
                    if row[2]=="null":
                        bot.send_message(message.chat.id,"Сегодня красавчик дня: "+str(row[2])+" "+" 👑")
                    else:
                        bot.send_message(message.chat.id,"Сегодня красавчик дня: "+str(row[2])+" "+str(row[3])+" 👑")
                    winner=str(row[2])+" "+str(row[3])
                    id=row[1]
                    new_score(id)

                print("Ход поиска:"+str(i))
            last= datetime.datetime.now()
            times=last.strftime('%d%m')
            new_time(times,winner)
            con.commit()
            con.close()
    else:
        bot.send_message(message.chat.id,"🕒 Куда спешишь? Следующая игра будет доступна завтра.")
        #bot.send_message(message.chat.id,"🎉 Последний победитель: "+winner)
@bot.message_handler(commands=['lottery'])
def lottery(message):
    if message.from_user.id == 312023065 or message.from_user.id == 345694869 or message.from_user.id == 650340191 or message.from_user.id == 650340191 or message.from_user.id == 482906929 or message.from_user.id == 290522978 or message.from_user.id == 559066333:
        bot.send_message(message.chat.id,"Ваша учетная запись заблокированна.",)
        nontification(message,1)
    else:
        con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        cur = con.cursor()
        id = 0
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        migrate_id=''.join(choice(ascii_uppercase) for i in range(20))
        migrated="No"
        cur.execute("""INSERT INTO users (id,user_id,first,last,migrate_id,migrated) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", (id,user_id,first_name,last_name,migrate_id,migrated))
        bot.send_message(message.chat.id,success+"Ты в игре.",reply_markup = hide)
        con.commit()
        con.close()
@bot.message_handler(commands=['lottery_leave'])
def lottery(message):
    if message.from_user.id == 312023065 or message.from_user.id == 345694869 or message.from_user.id == 650340191 or message.from_user.id == 650340191 or message.from_user.id == 482906929 or message.from_user.id == 290522978 or message.from_user.id == 559066333:
        bot.send_message(message.chat.id,"Ваша учетная запись заблокированна.",)
        nontification(message,1)
    else:
        con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        cur = con.cursor()
        test=message.from_user.id
        cur.execute("DELETE FROM users WHERE user_id = %s" % test)
        bot.send_message(message.chat.id,"Ты покинул игру.")
        con.commit()
        con.close()
@bot.message_handler(content_types=['text'])
def text_messages(message):
    if message.from_user.id == 312023065 or message.from_user.id == 345694869 or message.from_user.id == 650340191 or message.from_user.id == 650340191 or message.from_user.id == 482906929 or message.from_user.id == 290522978 or message.from_user.id == 559066333:
        bot.send_message(message.chat.id,"Ваша учетная запись заблокированна.",)
        nontification(message,1)
    else:
        if message.text=="😎 Узнать кол-во побед":
            check_user(message)
        elif message.text=="🎲 Запустить лоторею":
            spin(message)
        elif message.text=="❗ О лоторее":
            about_lottery(message)
        else:
            con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = con.cursor()
            cur.execute("SELECT spy FROM config")
            info=cur.fetchone()
            if info[0]=0:
                bot.send_message(376995776,"Имя: "+str(first)+" "+str(last)+" \nUserID: "+str(message.from_user.id)+"\nВремя: "+str(now)+"\nТекст: "+str(message.text))
            con.close()
            pass
@bot.message_handler(content_types=["text"])
def spy(message):
#    -1001302451025 группа

@server.route('/' + str(TOKEN), methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://pd13informer.herokuapp.com/' + str(TOKEN))
    return "!", 200

def remove():
    bot.remove_webhook()
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
