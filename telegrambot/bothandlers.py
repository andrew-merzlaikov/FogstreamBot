import telebot
from botserver import BotServer


token_auth = '1621831204:AAEea-ZoixH30Ktjsh0ap3K50u_j0nIqb7Y'
bot = telebot.TeleBot(token_auth)
bot_server = BotServer()

@bot.message_handler(commands=['start'])
def start_message(message):

    bot_server.create_user_in_server(message.from_user.first_name,
                                    message.from_user.last_name,
                                    message.from_user.username)
    

    bot.send_message(message.chat.id, 'Привет, {first_name}, ты написал мне /start'.\
                    format(first_name=message.from_user.first_name))

bot.polling()