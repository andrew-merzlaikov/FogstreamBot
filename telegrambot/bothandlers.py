import telebot
from botserver import BotServer
import config

bot = telebot.TeleBot(config.token_auth)
bot_server = BotServer()

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "begin")
