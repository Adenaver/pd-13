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
from top import top_list
from random import choice
from string import ascii_uppercase
from update_score import new_score
from update_time import new_time
TOKEN = os.environ.get('TOKEN')
hostname = os.environ.get('hosting')
username = os.environ.get('user')
password = os.environ.get('password')
database = os.environ.get('dbname')
unaviable = u'\U0001F512' # unaviable
success = u'\U00002705' # unaviable
close = u'\U0000274C' # unaviable
sby= u'\U0001F4E1' # sby text 1F4DD
rashif = u'\U0001F4DD' # расшифровка сбу
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
schedule_markup = telebot.types.ReplyKeyboardMarkup(True, False)
schedule_markup.row('Сегодня', 'Завтра')
keyboard = telebot.types.InlineKeyboardMarkup()
callback_button = telebot.types.InlineKeyboardButton(text="Расписание(Сегодня)", callback_data="today")
callback_button_test = telebot.types.InlineKeyboardButton(text="Состояние", callback_data="status")
keyboard.add(callback_button,callback_button_test)
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
date_one= "07.06.2018"
group_data = '913'
def parsing_timetable(call):
    bot.send_message(call.message.chat.id, "🚫 Летом данная функция не доступна.")
    """
    today = datetime.datetime.now()
    date_one= today.strftime("%d.%m.%Y")
    date_two = today.strftime("%d.%m.%Y")
    schedule_url='http://e-rozklad.dut.edu.ua/timeTable/group?TimeTableForm%5Bfaculty%5D=1&TimeTableForm%5Bcourse%5D=1&TimeTableForm%5Bgroup%5D=913&TimeTableForm%5Bdate1%5D={}&TimeTableForm%5Bdate2%5D={}&TimeTableForm%5Br11%5D=5&timeTable=0'.format(date_one,date_one)
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
        week= datetime.datetime.today().weekday()
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
        if len(day[week])==0:
            bot.send_message(call.message.chat.id,"Пар не обнаруженно.")
        """
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "today":
            #bot.send_message(call.message.chat.id, "Еее")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Лови!")
            parsing_timetable(call)
        elif call.data == "status":
            bot.send_message(call.message.chat.id, "Статус: ОК")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Держи!")
        elif call.data == "lottery":
            lottery(call)
@bot.message_handler(commands=['menu'])
def ss(message):
    bot.send_message(message.chat.id,"Выбери что тебе нужно сделать:",reply_markup=keyboard)
@bot.message_handler(commands=['about_lottery'])
def about_lottery(message):
    bot.send_message(message.chat.id,"Игра в которой, ты можешь испытать свою удачу.\n Каждый день выбирается рандомно красавчик дня")
    bot.send_message(message.chat.id,"Команды: \n /lottery - участвовать в игре\n /lottery_leave - покинуть игру")
@bot.message_handler(commands=['top'])
def top_lst(message):
    top_list(message)
@bot.message_handler(commands=['setnull'])
def nulled(message):
    if message.from_user.id== 376995776:
        db = shelve.open("config.txt")
        bot.send_message(message.chat.id,"✨ Время сброшено.")
        now=datetime.datetime.now()
        now_1=now.strftime('%d%m')
        now_1=-100
        db['time']=now_1
        db['winner']="NULL"
        db.sync()
        db.close()
    else:
        bot.send_message(message.chat.id,"🔒 У тебя нет прав на эту команду.")
        print(mes)
@bot.message_handler(commands=['remove'])
def nulled(message):
    if message.from_user.id== 376995776:
        remove()
    else:
        bot.send_message(message.chat.id,"🔒 У тебя нет прав на эту команду.")
        print(mes)
@bot.message_handler(commands=['s'])
def status(message):
    print(message.chat.id)
@bot.message_handler(commands=['my_wins'])
def check_user(message):
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
    con.commit()
    con.close()
@bot.message_handler(commands=['check_users'])
def check_user(message):
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    while True:
        row = cur.fetchone()
        if row == None:
            break
        elif row[3]==None:
            bot.send_message(message.chat.id,"🚨 У пользователя "+str(row[2])+" не заполненно поле Фамилия.")
    con.commit()
    con.close()
@bot.message_handler(commands=['spin'])
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
        bot.send_message(message.chat.id,"🚨 Внимание! С 14.07.2018 по 18.07.2018 будет технологическое окно. В 19,20,21 числах будут проведенны по 2 игры. 🚨")
        rand=random.randint(1,2)
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
                    new_score(id,counter)
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
                    new_score(id,counter)

                print("Ход поиска:"+str(i))
            last= datetime.datetime.now()
            times=last.strftime('%d%m')
            new_time(times,winner)
            con.commit()
            con.close()
    else:
        bot.send_message(message.chat.id,"🕒 Куда спешишь? Следующая игра будет доступна завтра.")
        #bot.send_message(message.chat.id,"🎉 Последний победитель: "+winner)
    db.sync()
    db.close()
@bot.message_handler(commands=['lottery'])
def lottery(message):
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    id = random.randint(0,30)
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    migrate_id=''.join(choice(ascii_uppercase) for i in range(20))
    migrated="No"
    cur.execute("""INSERT INTO users (id,user_id,first,last,migrate_id,migrated) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", (id,user_id,first_name,last_name,migrate_id,migrated))
    bot.send_message(message.chat.id,success+"Ты в игре.")
    con.commit()
    con.close()
@bot.message_handler(commands=['lottery_leave'])
def lottery(message):
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    test=message.from_user.id
    cur.execute("DELETE FROM users WHERE user_id = %s" % test)
    bot.send_message(message.chat.id,"Похоже ты покинул игру :(")
    con.commit()
    con.close()

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
