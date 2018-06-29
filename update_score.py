import psycopg2
import os
hostname = os.environ.get('hosting')
username = os.environ.get('user')
password = os.environ.get('password')
database = os.environ.get('dbname')
def new_score(id,counter):
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    score=0
    for i in range(counter):
        row = cur.fetchone()
        if row == None:
            print("Остановка поиска. Конец БД")
            break
        elif row[1]==test2:
            score=row[0]
            score+=1
    cur.execute("UPDATE users SET id = %s WHERE user_id = %s",(score,id))
    con.commit()
    con.close()
