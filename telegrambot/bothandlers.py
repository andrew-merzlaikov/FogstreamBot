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
        
    id_user = bot_server.\
              telegram_user_id_from_database(message.from_user.username,
                                            message.from_user.first_name,
                                            message.from_user.last_name)
    
    count_logic = bot_server.get_count_logic_entities()

    bot.send_message(message.chat.id, '{id_user}'.\
                                      format(id_user=id_user))

    for i in range(0, count_logic):
        data = bot_server.get_logic_entity(id_user)
        bot.send_message(message.chat.id, '{data}'.\
                        format(data=str(data)))
    

bot.polling()