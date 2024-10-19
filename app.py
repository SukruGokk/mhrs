from threading import Timer
from json import loads
from flask import Flask, request
from bot import Bot
import utils

app = Flask(__name__)

API_TOKEN = '7312371034:AAGZuZmtUkYgEUGmr-mbXsmN4VZmLAq0EtQ'
WEBHOOK_URL = 'https://dead-klara-sukruerdem-841b56dc.koyeb.app//update'

bot = Bot(API_TOKEN)
bot.webhook(WEBHOOK_URL)

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

rt = RepeatedTimer(90, utils.check_all, bot)

@app.route('/update', methods=['POST'])
def webhook():
    print(request.get_data())
    message = loads(request.get_data().decode('UTF-8'))
    bot.func(message)
    return 'ok', 200

if __name__ == '__main__':
    app.run()
