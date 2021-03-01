import telebot
from botserver import BotServer
import config
import enum

bot = telebot.TeleBot(config.token_auth)
bot_server = BotServer()


class CurrentMessage:
    data_message = None

# Поставь флаги для удобства
# 1 - Если на вопрос надо ответить вариантами ответа
# 2 - Если на вопрос надо ответить произвольно
# 3 - Если надо вывести сообщение

class Flag:
    STATE_MESSAGE = None

def handler_current_message(message, current_message):

    if current_message is not None:
        
        if current_message['message']['write_answer'] is True:
            options = bot_server.\
                    get_options_answers(current_message['message']['id'])  

            if options["options_answer"][0] is not None:
                Flag.STATE_MESSAGE = "1"
                
                bot.send_message(message.chat.id, 
                                 "{text}".\
                                 format(text=current_message["message"]['text_message']))

                bot.send_message(message.chat.id, 
                                "Варианты ответов {data}".\
                                format(data=options['options_answer']))
            
            else:
                Flag.STATE_MESSAGE = "2"
                
                bot.send_message(message.chat.id, 
                                 "{text}".\
                                 format(text=current_message["message"]['text_message']))

                bot.send_message(message.chat.id, 
                                "Введите ответ на вопрос")
        else:
            Flag.STATE_MESSAGE = "3"   

            id_current_message = CurrentMessage.data_message["message"]['id']

            if bot_server.get_check_end_tree(id_current_message):
                bot.send_message(message.chat.id, 
                        "{data}".format(data=CurrentMessage.\
                                             data_message["message"]["text_message"]))

                data_next_message = bot_server.get_next_message(id_current_message)
                CurrentMessage.data_message = data_next_message
                handler_current_message(message, CurrentMessage.data_message)
            else:
                bot.send_message(message.chat.id, 
                                "{data}".\
                                format(data=CurrentMessage.\
                                            data_message["message"]["text_message"]))
                        
                bot.send_message(message.chat.id, "Чтобы начать заново нажмите /start")
    

@bot.message_handler(commands=["start"])
def cmd_start(message): 
    
    response = bot_server.\
               create_user_in_server(message.from_user.id,
                                    message.from_user.username,
                                    message.from_user.first_name,
                                    message.from_user.last_name)
    
    data = bot_server.get_root_message()
    
    CurrentMessage.data_message = data
    
    handler_current_message(message, CurrentMessage.data_message)
    

# Здесь обрабатывается вопрос если у него есть варианты ответы
@bot.message_handler(func=lambda message: Flag.STATE_MESSAGE == "1")
def question_first_type_handler(message):

    answer_text = message.text
    root_message = None

    if CurrentMessage.data_message is not None:
        root_message = CurrentMessage.data_message['message']


        options = bot_server.\
                  get_options_answers(root_message['id'])  

        if message.text not in options['options_answer']:
            bot.send_message(message.chat.id, "Нет такого варианта ответа")      

        elif "id" in root_message.keys():
            
            id_current_message = root_message['id']

            data_next_message = bot_server.\
                                get_next_message(id_current_message,
                                                answer_text)

            if bot_server.get_check_end_tree(data_next_message["message"]["id"]):
                
                CurrentMessage.data_message = data_next_message
                
                handler_current_message(message, CurrentMessage.\
                                                 data_message)
            
            else:
                bot.send_message(message.chat.id, 
                             "{text}".\
                             format(text=data_next_message["message"]["text_message"]))   

                bot.send_message(message.chat.id, "Введите команду /start")

    else:
        bot.send_message(message.chat.id, "Введите команду /start")

@bot.message_handler(func=lambda message: Flag.STATE_MESSAGE == "2")
def question_second_type_handler(message):
    answer_text = message.text

    if CurrentMessage.data_message is not None:
        id_current_message = CurrentMessage.data_message['message']['id']
        
        data_next_message = bot_server.\
                            get_next_message(id_current_message,
                                            answer_text)
        
        print("QUESTION SECOND TYPE: ", data_next_message)

        if bot_server.get_check_end_tree(data_next_message["message"]["id"]):
                
            CurrentMessage.data_message = data_next_message

            
            handler_current_message(message, 
                                    CurrentMessage.\
                                    data_message)
            
        else:
            bot.send_message(message.chat.id, 
                             "{text}".\
                             format(text=data_next_message["message"]["text_message"]))   

            bot.send_message(message.chat.id, "Введите команду /start")
            


bot.polling()