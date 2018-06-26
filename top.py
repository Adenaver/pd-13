import requests
import psycopg2
import os
import telebot
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
hostname = os.environ.get('hosting')
username = os.environ.get('user')
password = os.environ.get('password')
database = os.environ.get('dbname')
def top_list(message):
    counter=0
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    max1=0
    name1=0
    id1=0
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            if row[0]>=max1:
                max1=row[0]
                name1=str(row[2])+" "+str(row[3])
                id1=row[1]
    bot.send_message(message.chat.id,"1 место: "+str(name1)+" Побед: "+str(max1)+" 👑")
    print("1 Макс число: "+str(max1))
    print("1 Имя: "+str(name1))
    con.commit()
    con.close()
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    max2=0
    name2=0
    id2=0
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            if row[1]!=id1:
                if row[0]>max2 and max1>=max2:
                    max2=row[0]
                    name2=str(row[2])+" "+str(row[3])
                    id2=row[1]
    bot.send_message(message.chat.id,"2 место: "+str(name2)+" Побед: "+str(max2)+" 👑")
    print("2 Макс число: "+str(max2))
    print("2 Имя: "+str(name2))
    con.commit()
    con.close()
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    max3=0
    name3=0
    id3=0
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            if row[1]!=id2 and row[1]!=id1:
                if row[0]>max3 and max2>=max3:
                    max3=row[0]
                    name3=str(row[2])+" "+str(row[3])
                    id3=row[1]
    bot.send_message(message.chat.id,"3 место: "+str(name3)+" Побед: "+str(max3)+" 👑")
    print("3 Макс число: "+str(max3))
    print("3 Имя: "+str(name3))
    con.commit()
    con.close()
