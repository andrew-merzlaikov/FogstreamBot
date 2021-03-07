#import telebot
from botserver import BotServer
import config
#import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio

"""
Илья Пятриков 
Асинхронный бот (потом сделаем merge наших веток)
"""

TOKEN = '1639370701:AAE-wsM4pNioUGoCdVcmqmXpQo2bAp8HWqo'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

#bot = telebot.TeleBot('1625427693:AAHWf0xwIQziquQFa78ofxHObHUT20lJLY8')
bot_server = BotServer()
token = bot_server.get_token()
user_id_db = {}
print(user_id_db)

async def checking_message(message, message_chat_id):
    """
    Функция определяет к какому варианту относится
    текущее сообщение. И соответственно обрабатывает
    это сообщение.
    """

    print("USER_ID_DB:", user_id_db)
    
    # получаем текущее сообщение с базы данных
    cur_mess = bot_server.get_current_message(message.from_user.id)
    
    count_child = bot_server.get_count_child(cur_mess['id'])

    # определяем, что сообщение является вопросом, но в дереве диалога последнее
    # этом варианте события, ответ пользователя заранее не определён и является произвольным
    # нужно его вывести и соответствующим обработчиком принять ответ от пользова    
    if cur_mess['write_answer'] == True and count_child == 0:        
        await bot.send_message(message_chat_id, cur_mess['text_message'])
	# флаг принимает значение для срабатывания соответствующего обработчика
        user_id_db[str(message.chat.id)] = 1
		
    # определяем, что сообщение является вопросом и есть следущее сообщение
    # тут так же ответ пользователя заранее не определён и является произвольным
    # следущее сообщение будет без вариантов, то есть у данного сообщения один потомок	
    if cur_mess['write_answer'] == True and count_child == 1:    
        await bot.send_message(message_chat_id, cur_mess['text_message'])
        user_id_db[str(message.chat.id)] = 2

    # определяем, что сообщение является вопросом и потомоков более одного
    # этом варианте события, где ответ пользователя заранее определён заданными вариантами
    if cur_mess['write_answer'] == True and count_child > 1:        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = cur_mess['options_answer']
        print(buttons)
        keyboard.add(*buttons)
        await bot.send_message(message_chat_id, cur_mess['text_message'], reply_markup=keyboard)              
        user_id_db[str(message.chat.id)] = 3

    # определяем, что сообщение не является вопросом и потомоков более одного
    # это ошибочное состояние, не верно указано логика администратором бота
    # если потомка более одного, значит нужно выбрать один из них
    # то есть пользовательдолжен дать ответ, а это означает
    # что сообщение должно являеться вопросом
    if cur_mess['write_answer'] == False and count_child > 1:
        #print("['write_answer'] == False and count_child == 0")
        #print(cur_mes.data)
        print("cur_mes.data['write_answer'] == False and count_child > 2")
        print("Для сообщения имеющего двух потомков не указано, что это вопрос")
   
		
    # определяем, что сообщение не является вопросом и потомок один
    # если таких сообщений несколько подряд, то они будут
    # выводится один за другим, разделяемые указаной задержкой
    while cur_mess['write_answer'] == False and count_child == 1:
        await bot.send_message(message_chat_id, cur_mess['text_message'])
        await asyncio.sleep(cur_mess['delay'])
        # когда берем следующее собщение, то следующее сообщение 
        # устанавливается как текущее
        bot_server.get_next_fullmessage(message.from_user.id, 
                                        cur_mess['id'])
        cur_mess = bot_server.get_current_message(message.from_user.id)
        count_child = bot_server.get_count_child(cur_mess['id'])

    # определяем, что сообщение не является вопросом и потомоков нет
    # следовательно, это последнее сообщение в дереве диалога
    if cur_mess['write_answer'] == False and count_child == 0:
        await bot.send_message(message_chat_id, cur_mess['text_message'])
        await asyncio.sleep(15)
        await bot.send_message(message_chat_id, "Чтобы вновь начать диалог - введите /start")



async def main():
    
    @dp.message_handler(commands=['help'])        
    async def cmd_help(message: types.Message):
        mes = 'Команда /start начинает диалог с начала.\n' +\
              'Команда /help выводит информацию о боте и командах.'   
        await bot.send_message(message.from_user.id, mes)	



    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message): 
        """
        Обработчик для команды /start
        """
        await asyncio.sleep(3)
        # Когда создаем пользователя на сервере, то устанавливается
        # корневое сообщение в качестве текущего
        bot_server.create_user_in_server(message.from_user.id,
                                        message.from_user.username,
                                        message.from_user.first_name,
                                        message.from_user.last_name)
        
        # когда берем следующее собщение, то следующее сообщение 
        # устанавливается как текущее
        bot_server.get_next_fullmessage(message.from_user.id)    
        await checking_message(message, message.from_user.id)
 

    # сработает, если сообщение является вопросом, но в дереве диалога последнее
    @dp.message_handler(lambda message: user_id_db[str(message.chat.id)] == 1)
    async def question_and_zero_followers(message: types.Message):
        await asyncio.sleep(3) 
        cur_mess = bot_server.get_current_message(message.from_user.id)
        bot_server.set_answer_user(message.from_user.id, cur_mess['id'], message.text)	
        await asyncio.sleep(15)	
        await bot.send_message(message.from_user.id, "Чтобы вновь начать диалог - введите /start")


    # сработает, если сообщение является вопросом и есть следущее сообщение
    @dp.message_handler(lambda message: user_id_db[str(message.chat.id)] == 2)
    async def question_and_one_follower(message: types.Message):
        await asyncio.sleep(3) 
        # берем текущее сообщение с сервера
        cur_mess = bot_server.get_current_message(message.from_user.id)
        bot_server.set_answer_user(message.from_user.id, cur_mess['id'], message.text)

        if cur_mess['delay'] != 0:
            await bot.send_message(message.from_user.id, "Пожалуйста, немного подождите")
            await asyncio.sleep(cur_mess['delay'])	

        # когда берем следующее собщение, то следующее сообщение 
        # устанавливается как текущее
        bot_server.get_next_fullmessage(message.from_user.id,
                                                       cur_mess['id'])
        await checking_message(message, message.from_user.id)


    # сработает, если сообщение является вопросом и потомоков более одного
    @dp.message_handler(lambda message: user_id_db[str(message.chat.id)] == 3)
    async def question_and_multiple_followers(message: types.Message):
        await asyncio.sleep(3)
        # все варианты ответов переводим в нижний регистр
        cur_mess = bot_server.get_current_message(message.from_user.id)
        options_answer = [x.lower() for x in cur_mess['options_answer']]

        if message.text.lower() in options_answer:
            bot_server.set_answer_user(message.from_user.id, cur_mess['id'], message.text)	
            if cur_mess['delay'] != 0:
                await bot.send_message(message.from_user.id, "Пожалуйста, немного подождите")
                await asyncio.sleep(cur_mess['delay'])	
            
            # когда берем следующее собщение, то следующее сообщение 
            # устанавливается как текущее
            bot_server.get_next_fullmessage(message.from_user.id, 
                                            cur_mess['id'], 
                                            message.text)

            await checking_message(message, message.from_user.id)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = cur_mess['options_answer']
            keyboard.add(*buttons)
            await bot.send_message(message.from_user.id, "Выбран не существующий вариант, попробуйте ещё раз.", reply_markup=keyboard )

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())




    

   

























