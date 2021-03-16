from botserver import BotServer
from botflag import BotFlag

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import ValidationError
import asyncio
import logging


logging.basicConfig(filename='bot.log', filemode='w')

# BotServer содержит методы, которые выполняют запросы к БД
bot_server = BotServer()
TOKEN = bot_server.get_token()['token']

try:
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
except ValidationError:
    logging.error("Администратор указал не верный токен")
    print("Администратор указал не верный токен")
    exit()

# BotFlag() позволяет устанавливать и получать
# флаг текущего типа вопроса для каждого пользователя 
bot_flag = BotFlag()


async def checking_message(ms_chat_id):
    """
    Функция определяет к какому варианту относится
    текущее сообщение. И соответственно обрабатывает
    это сообщение.
    :param ms_chat_id: уникальный номер пользователя
    :type ms_chat_id: int
    """
    
    # получаем текущее сообщение с базы данных
    cur_mes = bot_server.get_current_message(ms_chat_id)

    # получаем количество потомков для данного сообщения
    count_child = bot_server.get_count_child(cur_mes['id'])

    # определяем, что сообщение не является вопросом и потомок один
    # если таких сообщений несколько подряд, то они будут
    # выводится один за другим, разделяемые указаной задержкой
    while cur_mes['write_answer'] is False and count_child == 1:
        await bot.send_message(ms_chat_id, cur_mes['text_message'])
        await asyncio.sleep(cur_mes['delay'])
        # устанавливает в БД в качестве нового текущего
        # сообщения, номер потомка текущего сообщения
        bot_server.get_next_fullmessage(ms_chat_id, 
                                        cur_mes['id'])
        # получаем запись уже с новым текущим сообщением
        # для текущего пользователя
        cur_mes = bot_server.get_current_message(ms_chat_id)
        count_child = bot_server.get_count_child(cur_mes['id'])

    # определяем, что сообщение является вопросом, но в дереве
    # диалога последнее
    # в этом варианте события, ответ пользователя заранее
    # не определён и является произвольным
    # текущее сообщение нужно вывести и соответствующим
    # обработчиком принять ответ от пользователя
    if cur_mes['write_answer'] is True and count_child == 0:
        await bot.send_message(ms_chat_id, cur_mes['text_message'])
        # флаг принимает значение для срабатывания
        # соответствующего обработчика
        bot_flag.set_flag_user(ms_chat_id, 1)

    # определяем, что сообщение является вопросом
    # и есть следущее сообщение
    # тут так же ответ пользователя заранее не определён
    # и является произвольным
    # следущее сообщение будет без вариантов,
    # то есть у данного сообщения один потомок
    if cur_mes['write_answer'] is True and count_child == 1:
        await bot.send_message(ms_chat_id, cur_mes['text_message'])
        bot_flag.set_flag_user(ms_chat_id, 2)

    # определяем, что сообщение является вопросом
    # и потомоков более одного
    # этом варианте события, где ответ пользователя
    # заранее определён заданными вариантами
    if cur_mes['write_answer'] is True and count_child > 1:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                             one_time_keyboard=True)
        buttons = cur_mes['options_answer']
        keyboard.add(*buttons)
        await bot.send_message(ms_chat_id, cur_mes['text_message'],
                               reply_markup=keyboard)
        bot_flag.set_flag_user(ms_chat_id, 3)

    # определяем, что сообщение не является вопросом
    # и потомоков более одного
    # это ошибочное состояние, не верно указано логика
    # администратором бота
    # если потомка более одного, значит нужно выбрать один из них
    # то есть пользовательдолжен дать ответ, а это означает
    # что сообщение должно являеться вопросом
    if cur_mes['write_answer'] is False and count_child > 1:
        await bot.send_message(ms_chat_id, cur_mes['text_message'])
        await bot.send_message(ms_chat_id, "Для сообщения имеющего "
                                  "более одного потомка не указано,"
                                 "что это сообщение является вопросом")
        print("Для сообщения имеющего более одного потомка не указано,"
              " что это сообщение является вопросом")
        logging.error("Для сообщения имеющего более одного потомка"
                    " не указано, что это сообщение является вопросом")

    # определяем, что сообщение не является вопросом и потомоков нет
    # следовательно, это последнее сообщение в дереве диалога
    if cur_mes['write_answer'] is False and count_child == 0:
        await bot.send_message(ms_chat_id, cur_mes['text_message'])
        await asyncio.sleep(15)
        await bot.send_message(ms_chat_id, "Начать диалог заново"
                                    " - /start. Справка - /help.")


async def main():
    
    # обработчик команды /help
    @dp.message_handler(commands=['help'])        
    async def cmd_help(message: types.Message):
        mes = 'Команда /start начинает диалог с начала.\n' +\
              'Команда /help выводит информацию о боте и командах.'   
        await bot.send_message(message.chat.id, mes)	

    # обработчик команды /start
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message): 
        await asyncio.sleep(3)
        # когда создаем пользователя на сервере, то устанавливается
        # первое сообщение в качестве текущего
        bot_server.create_user_in_server(message.chat.id,
                                        message.from_user.username,
                                        message.from_user.first_name,
                                        message.from_user.last_name)

        # вызываем функцию проверки типа сообщения
        # message.chat.id содержит уникальный номер пользователя
        await checking_message(message.chat.id)
 
    # сработает, если сообщение является вопросом,
    # но в дереве диалога последнее
    @dp.message_handler(lambda message:
                        bot_flag.get_flag_user(message.chat.id) == 1)
    async def question_and_zero_followers(message: types.Message):
        await asyncio.sleep(3) 
        # получаем для пользователя message.chat.id
        # запись его текущего сообщения
        cur_mes = bot_server.get_current_message(message.chat.id)
        # записываем в БД ответ пользователя message.chat.id
        bot_server.set_answer_user(message.chat.id,
                                   cur_mes['id'], message.text)
        await asyncio.sleep(15)	
        await bot.send_message(message.chat.id,
                    "Начать диалог заново - /start. Справка - /help.")

    # сработает, если сообщение является вопросом
    # и есть следущее сообщение, один потомок
    @dp.message_handler(lambda message:
                        bot_flag.get_flag_user(message.chat.id) == 2)
    async def question_and_one_follower(message: types.Message):
        await asyncio.sleep(3) 
        # берем текущее сообщение с сервера
        cur_mes = bot_server.get_current_message(message.chat.id)
        bot_server.set_answer_user(message.chat.id,
                                   cur_mes['id'], message.text)

        if cur_mes['delay'] > 10:
            await bot.send_message(message.chat.id,
                                   "Пожалуйста, немного подождите")
            await asyncio.sleep(cur_mes['delay'])	

        # следующее сообщение устанавливается текущим
        bot_server.get_next_fullmessage(message.chat.id, cur_mes['id'])
        # вызываем определение типа следущего сообщения
        await checking_message(message.chat.id)

    # сработает, если сообщение является вопросом
    # и потомоков более одного
    @dp.message_handler(lambda message:
                        bot_flag.get_flag_user(message.chat.id) == 3)
    async def question_and_multiple_followers(message: types.Message):
        await asyncio.sleep(3)        
        cur_mes = bot_server.get_current_message(message.chat.id)
        # все варианты ответов переводим в нижний регистр
        options_answer = [x.lower() for x in cur_mes['options_answer']]
        # проверяем чтобы пользователь ввел
        # существующий вариант ответа
        if message.text.lower() in options_answer:
            bot_server.set_answer_user(message.chat.id,
                                       cur_mes['id'], message.text)
            if cur_mes['delay'] > 10:
                await bot.send_message(message.chat.id,
                                       "Пожалуйста, немного подождите")
                await asyncio.sleep(cur_mes['delay'])	
            
            # в таблице БД пользователей указан номер сообщения,
            # которое для пользователя является текущим
            # bot_server.get_next_fullmessage принимает номер
            # текущего сообщения и устанавливает в БД, что
            # теперь текущим сообщением становится
            # следующее сообщение, то есть потомок текущего
            # сообщения, если потомок не один
            # то он устанавливается исходя из ответа
            # на текущее сообщение
            bot_server.get_next_fullmessage(message.chat.id, 
                                            cur_mes['id'], 
                                            message.text)

            await checking_message(message.chat.id)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=True)
            buttons = cur_mes['options_answer']
            keyboard.add(*buttons)
            await bot.send_message(message.chat.id,
                  "Выбран не существующий вариант,"
                  " попробуйте ещё раз.", reply_markup=keyboard)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
