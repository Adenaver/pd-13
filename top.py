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
    bot.send_message(message.chat.id,"1): "+str(name1)+" Побед: "+str(max1)+" 🥇")
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
    bot.send_message(message.chat.id,"2): "+str(name2)+" Побед: "+str(max2)+" 🥈")
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
    bot.send_message(message.chat.id,"3): "+str(name3)+" Побед: "+str(max3)+" 🥉")
    print("3 Макс число: "+str(max3))
    print("3 Имя: "+str(name3))
    con.commit()
    con.close()
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    max4=0
    name4=0
    id4=0
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            if row[1]!=id2 and row[1]!=id1 and row[1]!=id3:
                if row[0]>max4 and max3>=max4:
                    max4=row[0]
                    name4=str(row[2])+" "+str(row[3])
                    id4=row[1]
    bot.send_message(message.chat.id,"4): "+str(name4)+" Побед: "+str(max4))
    print("4 Макс число: "+str(max4))
    print("4 Имя: "+str(name4))
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    max5=0
    name5=0
    id5=0
    while True:
        row = cur.fetchone()
        if row == None:
            break
        else:
            if row[1]!=id2 and row[1]!=id1 and row[1]!=id3 and row[1]!=id4:
                if row[0]>max5 and max4>=max5:
                    max5=row[0]
                    if row[3]="None":
                        name5=str(row[2]))
                    else:
                        name5=str(row[2])+" "+str(row[3])
                    id5=row[1]
    bot.send_message(message.chat.id,"5): "+str(name5)+" Побед: "+str(max5))
    print("5 Макс число: "+str(max5))
    print("5 Имя: "+str(name5))
    con.commit()
    con.close()
