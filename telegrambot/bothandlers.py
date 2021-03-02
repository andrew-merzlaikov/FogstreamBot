import telebot
from botserver import BotServer
import config
import enum

bot = telebot.TeleBot(config.token_auth)
bot_server = BotServer()
token = bot_server.get_token()
delay = bot_server.get_delay_message(58)

print("TOKEN = ", token)
print("DELAY = ", delay)

"""
1 - Состояние если вопрос и есть варианты ответа
2 - Состояние если вопрос и произвольный ответ
3 - Состояние если сообщение
"""

class CurrentMessage:
    data_message = None


class Flag:
    STATE_MESSAGE = None


def handler_current_message(message, current_message):
    """
    Функция, которая определяет какой флаг надо ставить
    Также в этой функции распечатывается текст сообщений
    и варианты ответа
    """

    # Если текущее сообщение не установлено
    if current_message is not None:
        
        # Если write_answer это True то значит это вопрос
        if current_message['message']['write_answer'] is True:
            options = bot_server.\
                    get_options_answers(current_message['message']['id'])  
            
            # Если первый элемент списке не None значит есть варианты
            # ответа

            print(options)

            if options["options_answer"] is not None:
                Flag.STATE_MESSAGE = "1"
                
                bot.send_message(message.chat.id, 
                                 "{text}".\
                                 format(text=current_message["message"]['text_message']))

                bot.send_message(message.chat.id, 
                                "Варианты ответов {data}".\
                                format(data=options['options_answer']))
            
            # Если вариантов нет, то значит ответ на этот вопрос 
            # произвольный и он обрабатывается соответствующим хэндлером
            else:
                Flag.STATE_MESSAGE = "2"
                
                bot.send_message(message.chat.id, 
                                 "{text}".\
                                 format(text=current_message["message"]['text_message']))

                bot.send_message(message.chat.id, 
                                "Введите ответ на вопрос")
        # значит текущее сообщение это обычный вопрос
        else:
            Flag.STATE_MESSAGE = "3"   

            id_current_message = CurrentMessage.data_message["message"]['id']
            
            # Проверяется является ли сообщение конечным
            if bot_server.get_check_end_tree(id_current_message):
                bot.send_message(message.chat.id, 
                        "{data}".format(data=CurrentMessage.\
                                             data_message["message"]["text_message"]))

                data_next_message = bot_server.get_next_message(id_current_message)
                CurrentMessage.data_message = data_next_message

                # Вызывается чтобы понять какой флаг надо ставить для следующего сообщения

                handler_current_message(message, CurrentMessage.data_message)
            # Если сообщение конечное, то мы выводим это сообщение
            # а после просим нажать /start
            else:
                bot.send_message(message.chat.id, 
                                "{data}".\
                                format(data=CurrentMessage.\
                                            data_message["message"]["text_message"]))
                        
                bot.send_message(message.chat.id, "Чтобы начать заново нажмите /start")
    

@bot.message_handler(commands=["start"])
def cmd_start(message): 
    """
    Обработчик для команды /start
    """
    response = bot_server.\
               create_user_in_server(message.from_user.id,
                                    message.from_user.username,
                                    message.from_user.first_name,
                                    message.from_user.last_name)
    
    data = bot_server.get_root_message()
    
    CurrentMessage.data_message = data
    
    handler_current_message(message, CurrentMessage.data_message)
    

@bot.message_handler(func=lambda message: Flag.STATE_MESSAGE == "1")
def question_first_type_handler(message):

    answer_text = message.text
    root_message = None

    # Проверяется установлено ли текущее сообщение
    if CurrentMessage.data_message is not None:
        root_message = CurrentMessage.data_message['message']


        options = bot_server.\
                  get_options_answers(root_message['id'])  

        # Если нет такого ответа среди вариантов выводим сообщение пользователю
        if message.text not in options['options_answer']:
            bot.send_message(message.chat.id, "Нет такого варианта ответа")      

        elif "id" in root_message.keys():
            
            id_current_message = root_message['id']


            # Проверяется является ли вопрос конечным
            if bot_server.get_check_end_tree(id_current_message):
                
                data_next_message = bot_server.\
                                    get_next_message(id_current_message,
                                                    answer_text)

                CurrentMessage.data_message = data_next_message
                
                # Вызывается чтобы понять какой флаг надо ставить для следующего сообщения

                handler_current_message(message, CurrentMessage.\
                                                 data_message)
            
            # Если это последнее сообщение выводим /start

            else:
                bot.send_message(message.chat.id, 
                             "{text}".\
                             format(text=CurrentMessage.\
                                         data_message["message"]["text_message"]))   

                bot.send_message(message.chat.id, "Введите команду /start")

    # Иначе просим ввести /start
    else:
        bot.send_message(message.chat.id, "Введите команду /start")

@bot.message_handler(func=lambda message: Flag.STATE_MESSAGE == "2")
def question_second_type_handler(message):
    answer_text = message.text
    print("Flag.STATE_MESSAGE=", Flag.STATE_MESSAGE)

    # Проверяем установлено ли текущее сообщение
    if CurrentMessage.data_message is not None:
        id_current_message = CurrentMessage.data_message['message']['id']
        
    
        # Проверяется является ли вопрос конечным
        if bot_server.get_check_end_tree(id_current_message):
        
            data_next_message = bot_server.\
                                get_next_message(id_current_message,
                                                answer_text)

            CurrentMessage.data_message = data_next_message

            # Вызывается чтобы понять какой флаг надо ставить для следующего сообщения
            handler_current_message(message, 
                                    CurrentMessage.\
                                    data_message)

        # Если вопрос конечный, то выводим его и просим ввести /start 
        else:   

            bot.send_message(message.chat.id, "Введите команду /start")
            


bot.polling()