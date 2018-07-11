import telebot
import datetime
TOKEN = os.environ.get('TOKEN')
hostname = os.environ.get('hosting')
username = os.environ.get('user')
password = os.environ.get('password')
database = os.environ.get('dbname')
bot = telebot.TeleBot(TOKEN)
def lottery_ready():
    last= datetime.datetime.now()
    now_time=last.strftime('%d%m')
    id=123
    cur.execute("SELECT last_time FROM times WHERE user_id = %s",(id,))
    row=cur.fetchone()
    if now_time!=row[0]:
        bot.send_message(-1001302451025,"Игра снова доступна. /spin")
    else:
        pass
def lottery_ready()
