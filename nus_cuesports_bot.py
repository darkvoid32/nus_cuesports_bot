import os
import telegram
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN')
BOT_USER_NAME = os.environ.get('BOT_USER_NAME')
URL = ""

bot = telegram.Bot(token=BOT_API_TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(BOT_API_TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)

   if text == "/start":
       bot_welcome = """Welcome to NUS Cuesports!"""

       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


   else:
       try:
           bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)
       except Exception as e:
           bot.sendMessage(chat_id=chat_id, text="Exception occured: " + e, reply_to_message_id=msg_id)

   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=BOT_API_TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)