from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config
from botserver import BotServer

bot = Bot(token=config.token_auth)
dp = Dispatcher(bot)

bot_server = BotServer()
token = bot_server.get_token()
delay = bot_server.get_delay_message(141)

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


async def handler_current_message(message, current_message):
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
            print(options["options_answer"])

            if options["options_answer"] is not None:
                Flag.STATE_MESSAGE = "1"
                
                await bot.send_message(message.chat.id, 
                                      "{text}".\
                                       format(text=current_message["message"]['text_message']))

                await bot.send_message(message.chat.id, 
                                      "Варианты ответов {data}".\
                                      format(data=options['options_answer']))
            
            # Если вариантов нет, то значит ответ на этот вопрос 
            # произвольный и он обрабатывается соответствующим хэндлером
            else:
                Flag.STATE_MESSAGE = "2"
                
                await bot.send_message(message.chat.id, 
                                        "{text}".\
                                        format(text=current_message["message"]['text_message']))

                await bot.send_message(message.chat.id, 
                                       "Введите ответ на вопрос")
        # значит текущее сообщение это обычный вопрос
        else:
            Flag.STATE_MESSAGE = "3"   

            id_current_message = CurrentMessage.data_message["message"]['id']
            
            # Проверяется является ли сообщение конечным
            if bot_server.get_check_end_tree(id_current_message):
                await bot.send_message(message.chat.id, 
                                      "{data}".format(data=CurrentMessage.\
                                                           data_message["message"]["text_message"]))

                data_next_message = bot_server.get_next_message(id_current_message)
                bot_server.get_next_fullmessage(id_current_message)
                CurrentMessage.data_message = data_next_message

                # Вызывается чтобы понять какой флаг надо ставить для следующего сообщения

                handler_current_message(message, CurrentMessage.data_message)
            # Если сообщение конечное, то мы выводим это сообщение
            # а после просим нажать /start
            else:
                await bot.send_message(message.chat.id, 
                                    "{data}".\
                                    format(data=CurrentMessage.\
                                                data_message["message"]["text_message"]))
                        
                await bot.send_message(message.chat.id, "Чтобы начать заново нажмите /start")
    

@dp.message_handler(commands=["start"])
async def cmd_start(message): 
    """
    Обработчик для команды /start
    """
    response = bot_server.\
               create_user_in_server(message.from_user.id,
                                    message.from_user.username,
                                    message.from_user.first_name,
                                    message.from_user.last_name)
    
    data = bot_server.get_next_message()
    bot_server.get_next_fullmessage()
    

    CurrentMessage.data_message = data
    
    handler_current_message(message, CurrentMessage.data_message)
    

@dp.message_handler(func=lambda message: Flag.STATE_MESSAGE == "1")
async def question_first_type_handler(message):

    answer_text = message.text
    root_message = None

    # Проверяется установлено ли текущее сообщение
    if CurrentMessage.data_message is not None:
        root_message = CurrentMessage.data_message['message']


        options = bot_server.\
                  get_options_answers(root_message['id'])  

        print(options["options_answer"])

        # Если нет такого ответа среди вариантов выводим сообщение пользователю
        if message.text not in options['options_answer']:
            await bot.send_message(message.chat.id, "Нет такого варианта ответа")      

        elif "id" in root_message.keys():
            
            id_current_message = root_message['id']


            # Проверяется является ли вопрос конечным
            if bot_server.get_check_end_tree(id_current_message):
                
                data_next_message = bot_server.\
                                    get_next_message(id_current_message,
                                                     answer_text)
                bot_server.\
                get_next_fullmessage(id_current_message,
                                     answer_text)

                count = bot_server.\
                    get_count_child(id_current_message)
                    
                print("COUNT", count)

                # Установка ответа
                bot_server.set_answer_user(message.from_user.id,
                                           id_current_message,
                                           answer_text)
                
                CurrentMessage.data_message = data_next_message
                
                # Вызывается чтобы понять какой флаг надо ставить для следующего сообщения

                handler_current_message(message, CurrentMessage.\
                                                 data_message)
            
            # Если это последнее сообщение выводим /start

            else:
                await bot.send_message(message.chat.id, 
                                      "{text}".\
                                      format(text=CurrentMessage.\
                                                  data_message["message"]["text_message"]))   

                await bot.send_message(message.chat.id, "Введите команду /start")

    # Иначе просим ввести /start
    else:
        await bot.send_message(message.chat.id, "Введите команду /start")

@dp.message_handler(func=lambda message: Flag.STATE_MESSAGE == "2")
async def question_second_type_handler(message):
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
            # Установка ответа
            bot_server.set_answer_user(message.from_user.id,
                                       id_current_message,
                                       answer_text)
            bot_server.\
            get_next_fullmessage(id_current_message,
                                 answer_text)

            count = bot_server.\
                    get_count_child(id_current_message)

            print("COUNT", count)

            CurrentMessage.data_message = data_next_message

            # Вызывается чтобы понять какой флаг надо ставить для следующего сообщения
            handler_current_message(message, 
                                    CurrentMessage.\
                                    data_message)

        # Если вопрос конечный, то выводим его и просим ввести /start 
        else:   
            await bot.send_message(message.chat.id, "Введите команду /start")
            

if __name__ == '__main__':
    executor.start_polling(dp)

