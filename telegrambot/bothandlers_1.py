import telebot
from botserver import BotServer
import config
import time

bot = telebot.TeleBot('1639370701:AAE-wsM4pNioUGoCdVcmqmXpQo2bAp8HWqo')
bot_server = BotServer()
token = bot_server.get_token()
#delay = bot_server.get_delay_message(58)

print("TOKEN = ", token)
#print("DELAY = ", delay)


class Flag:
    flag = None

flag = Flag


class CurrentMessage:
    data = None

current_message = CurrentMessage


def checking_message(message_chat_id):
    """
    Функция определяет к какому варианту относится
    текущее сообщение. И соответственно обрабатывает
    это сообщение.
    """
    count_child = bot_server.get_count_child(current_message.data['id'])

    # определяем, что сообщение является вопросом, но в дереве диалога последнее
    # этом варианте события, ответ пользователя заранее не определён и является произвольным
    # нужно его вывести и соответствующим обработчиком принять ответ от пользова    
    if current_message.data['write_answer'] == True and count_child == 0:        
        bot.send_message(message_chat_id, current_message.data['text_message'])
	# флаг принимает значение для срабатывания соответствующего обработчика
        flag.flag = 1
		
    # определяем, что сообщение является вопросом и есть следущее сообщение
    # тут так же ответ пользователя заранее не определён и является произвольным
    # следущее сообщение будет без вариантов, то есть у данного сообщения один потомок	
    if current_message.data['write_answer'] == True and count_child == 1:    
        bot.send_message(message_chat_id, current_message.data['text_message'])
        flag.flag = 2

    # определяем, что сообщение является вопросом и потомоков более одного
    # этом варианте события, где ответ пользователя заранее определён заданными вариантами
    if current_message.data['write_answer'] == True and count_child > 1:        
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = current_message.data['options_answer']
        print(current_message.data['text_message'])
        keyboard.add(*buttons)
        bot.send_message(message_chat_id, current_message.data['text_message'], reply_markup=keyboard)              
        flag.flag = 3

    # определяем, что сообщение не является вопросом и потомоков более одного
    # это ошибочное состояние, не верно указано логика администратором бота
    # если потомка более одного, значит нужно выбрать один из них
    # то есть пользовательдолжен дать ответ, а это означает
    # что сообщение должно являеться вопросом
    if current_message.data['write_answer'] == False and count_child > 2:
        #print("['write_answer'] == False and count_child == 0")
        #print(current_message.data)
        print("current_message.data['write_answer'] == False and count_child == 2")
        print("Для сообщения имеющего двух потомков не указано, что это вопрос")
        # bot.send_message(message_chat_id, )
        bot.send_message(message_chat_id, "Сообщение имеет двух потомков, но не указано, что оно является вопросом - Администратор должен исправит логику")
        bot.send_message(message_chat_id, "Чтобы вновь начать диалог - введите /start")    
		
    # определяем, что сообщение не является вопросом и потомок один
    # если таких сообщений несколько подряд, то они будут
    # выводится один за другим, разделяемые указаной задержкой
    if current_message.data['write_answer'] == False and count_child == 1:
        print("TEST")
        print(current_message.data['text_message'])
        bot.send_message(message_chat_id, current_message.data['text_message'])
        time.sleep(current_message.data['delay'])
        current_message.data = bot_server.get_next_fullmessage(current_message.data['id'])
        count_child = bot_server.get_count_child(current_message.data['id'])

    # определяем, что сообщение не является вопросом и потомоков нет
    # следовательно, это последнее сообщение в дереве диалога
    if current_message.data['write_answer'] == False and count_child == 0:
        bot.send_message(message_chat_id, current_message.data['text_message'])
        time.sleep(15)
        bot.send_message(message_chat_id, "Чтобы вновь начать диалог - введите /start")



        
@bot.message_handler(commands=["help"])
def cmd_help(message):
    mes = 'Команда /start начинает диалог с начала.\n' +\
          'Команда /help выводит информацию о боте и командах.'
    bot.send_message(message.chat.id, mes) 



@bot.message_handler(commands=["start"])
def cmd_start(message): 
    """
    Обработчик для команды /start
    """
    # time.sleep(3) 
    bot_server.create_user_in_server(message.from_user.id,
                                    message.from_user.username,
                                    message.from_user.first_name,
                                    message.from_user.last_name)

    current_message.data = bot_server.get_next_fullmessage()    
    checking_message(message.chat.id)
    

# сработает, если сообщение является вопросом, но в дереве диалога последнее
@bot.message_handler(func=lambda message: flag.flag == 1)
def question_and_zero_followers(message):
    print("FLAG 1")
    time.sleep(3) 
    bot_server.set_answer_user(message.from_user.id, current_message.data['id'], message.text)	
    time.sleep(15)	
    bot.send_message(message.chat.id, "Чтобы вновь начать диалог - введите /start")


# сработает, если сообщение является вопросом и есть следущее сообщение
@bot.message_handler(func=lambda message: flag.flag == 2)
def question_and_one_follower(message):
    print("FLAG 2")
    time.sleep(3) 
    bot_server.set_answer_user(message.from_user.id, current_message.data['id'], message.text)
    if current_message.data['delay'] != 0:
        bot.send_message(message.chat.id, "Пожалуйста, немного подождите")
        time.sleep(current_message.data['delay'])	
    current_message.data = bot_server.get_next_fullmessage(current_message.data['id'])
    checking_message(message.chat.id)


# сработает, если сообщение является вопросом и потомоков более одного
@bot.message_handler(func=lambda message: flag.flag == 3)
def question_and_multiple_followers(message):
    time.sleep(3)
    print("FLAG 3")
    # все варианты ответов переводим в нижний регистр
    options_answer = [x.lower() for x in current_message.data['options_answer']]
    if message.text.lower() in options_answer:
        bot_server.set_answer_user(message.from_user.id, current_message.data['id'], message.text)	
        if current_message.data['delay'] != 0:
            bot.send_message(message.chat.id, "Пожалуйста, немного подождите")
            time.sleep(current_message.data['delay'])	
        current_message.data = bot_server.get_next_fullmessage(current_message.data['id'], message.text)
        checking_message(message.chat.id)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = current_message.data['options_answer']
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, "Выбран не существующий вариант, попробуйте ещё раз.", reply_markup=keyboard )



bot.polling()
