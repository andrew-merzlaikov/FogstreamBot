import telebot
from botserver import BotServer
import config

bot = telebot.TeleBot(config.token_auth)
bot_server = BotServer()

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "begin")
    
    id_user = bot_server.\
              create_user_in_server(message.from_user.id,
                                    message.from_user.username,
                                    message.from_user.first_name,
                                    message.from_user.last_name)
    
    bot.send_message(message.chat.id, "{data}".format(data=id_user))

bot.polling()