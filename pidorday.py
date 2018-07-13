import telebot
import sqlite3
import datetime
import re
import datetime
import time
import schedule
import os
import random
import shelve
token = "548094730:AAFmOYNK4uKZsDp6imVUcBh3_jMm2ERKeKU"
bot = telebot.TeleBot(token)
unaviable = u'\U0001F512' # unaviable
success = u'\U00002705' # unaviable
close = u'\U0000274C' # unaviable
sby= u'\U0001F4E1' # sby text 1F4DD
rashif = u'\U0001F4DD' # расшифровка сбу
def log(message,answer):
    print("\n-----")
    from datetime import datetime
    print(datetime.now())
    print("Сообещние от {0} {1} (id={2})\nТекст: {3}".format(message.from_user.first_name,
                                                                message.from_user.last_name,
                                                                str(message.from_user.id),
                                                                message.text))
    print("Ответ:",answer)
def user_check(message):
    global validate
    con = sqlite3.connect('pidor.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE user_id=?", (message.from_user.id,))
    lel="SELECT * FROM user WHERE user_id=?", (message.from_user.id,)
    print(lel)
    """
    while True:
        row = cur.fetchone()
        if row == None:
            break
        if row[1]==376995776:
            print(message.from_user.id)
            validate=1
            return 1
            break
        if row != None:
            print(row)
    """
    con.commit()
    con.close()
@bot.message_handler(commands=['about_lottery'])
def about_lottery(message):
    bot.send_message(message.chat.id,"Игра в которой ты можешь испытать свою удачу.\n Каждый день в 12:00 выбирается рандомно кто красавчик, а кто пидор дня :D")
    bot.send_message(message.chat.id,"Команды: \n /lottery - участвовать в игре\n /lottery_leave - покинуть игру \n /check - проверить работу бота")
@bot.message_handler(commands=['spin_lottery'])
def spin(message):
    con = sqlite3.connect('time.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM time")
    row = cur.fetchone()
    last_update=row[0]
    con.commit()
    con.close()
    today = datetime.datetime.now()
    now=today.strftime('%H%M%S')
    db = shelve.open("config.txt")
    db['time']="132059"
    #db['time']=today.strftime('%H%M%S')
    info_bd=db['time']
    print(info_bd)
    print(now)
    if info_bd>now:
        rand=random.randint(1,2)
        if True:
            counter=0
            con = sqlite3.connect('pidor.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM user")
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                else:
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
            con = sqlite3.connect('pidor.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM user")
            for i in range(counter):
                row = cur.fetchone()
                if row == None:
                    print("Остановка поиска. Конец БД")
                    break
                if i==randomizer:
                    bot.send_message(message.chat.id,"Сегодня красавчик дня: "+row[2]+row[3])
                print("Ход поиска:"+str(i))
            db['time']= datetime.datetime.now()
            con.commit()
            con.close()
    else:
        bot.send_message(message.chat.id,"🕒 Куда спешишь? Ещё рано :О")
    db.sync()
    db.close()
@bot.message_handler(commands=['lottery'])
def lottery(message):
    global validate
    user_check(message)
    con = sqlite3.connect('pidor.db')
    cur = con.cursor()
    id = random.randint(0,30)
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    cur.execute("INSERT OR IGNORE INTO user VALUES (?, ?, ?, ?)", (id,user_id,first_name,last_name))
    bot.send_message(message.chat.id,success+"Ты в игре.")

        #bot.send_message(message.chat.id,close+"Ты уже участвуешь в игре.")
    con.commit()
    con.close()
@bot.message_handler(commands=['lottery_leave'])
def lottery(message):
    bot.send_message(message.chat.id,close+"Попробуй позже.")
    con = sqlite3.connect('pidor.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM user")
    while True:
        row = cur.fetchone()
        if row == None:
            break
        if row[1]==message.from_user.id:
            test=row[0]
    cur.execute("DELETE FROM user WHERE id = %s" % test)
    bot.send_message(message.chat.id,"Похоже ты покинул игру :(")
    con.commit()
    con.close()
@bot.message_handler(commands=['del'])
def lottery_check(message):
    bot.send_message(message.chat.id,"тест.Удаление через 10 сек.")
    time.sleep(2)
    bot.delete_message(message.chat.id,message.message_id+1)
    pass
def hi(controller):
    if controller == False:
        today = datetime.datetime.now()
        info_time = today.strftime("%H:%M")
        bot.send_message(message.chat.id,"["+info_time+"]"+ " Сервер начал работу (или был перезапущен).\nКоманды бота: /about_lottery ")
        controller = True
@bot.message_handler(commands=['check'])
def check(message):
    ran=random.randint(10,90)
    bot.send_message(message.chat.id,"Статус: Активен  |"+" Пинг: "+str(ran))
@bot.message_handler(commands=['devmode'])
def handle_start_help(message):
    if message.from_user.id == 376995776:
        bot.send_message(message.chat.id,"Привет, Zhenyokoff.\nВсю дебаг инфу скинул тебе в логи.")
    else:
        bot.send_message(message.chat.id,unaviable+"У тебя нету доступа к этому разделу :(")
        print(message.from_user.id)
if __name__ == '__main__':
    bot.polling(none_stop=True,interval=0)
# 0 понедельник 1 вторник 2 среда 3 четверг 4 пятница 5 субота 6 воскресенье
