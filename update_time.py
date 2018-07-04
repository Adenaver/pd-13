import psycopg2
import os
hostname = os.environ.get('hosting')
username = os.environ.get('user')
password = os.environ.get('password')
database = os.environ.get('dbname')
def new_time(time,winner):
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("UPDATE times SET last_time = %s WHERE user_id = 123",(time,id))
    cur.execute("UPDATE times SET last_win = %s WHERE user_id = 123",(winner,id))
    con.commit()
    con.close()
def test_insert():
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    last="null"
    user=123
    win="null"
    cur.execute("""INSERT INTO times (user_id,last_time,last_win) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING""", (user,last,win))
    con.commit()
    con.close()
test_insert()
