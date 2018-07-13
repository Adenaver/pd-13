import psycopg2
import os
#hostname = os.environ.get('hosting')
#username = os.environ.get('user')
#password = os.environ.get('password')
#database = os.environ.get('bdname')
hostname = "pellefant.db.elephantsql.com"
username = "axwihbpd"
password = "FAKqDfFgwFzn8-2Icl3IkXjp77eVuWSR"
database = "axwihbpd"
def new_score(id):
    id=str(id)
    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cur = con.cursor()
    score=0
    cur.execute("SELECT id FROM users WHERE user_id = %s",(id,))
    row = cur.fetchone()
    score=row[0]
    score+=1
    cur.execute("UPDATE users SET id = %s WHERE user_id = %s",(score,id))
    con.commit()
    con.close()
new_score(376995776)
