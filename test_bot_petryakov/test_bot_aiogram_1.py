
TOKEN = '1625427693:AAHWf0xwIQziquQFa78ofxHObHUT20lJLY8'

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



class State:
    flag = None


@dp.message_handler(commands=['start'])
async def mes1(message):
    ms = 'message_id: {} chat.id: {} from_user.id: {} from_user.username: {} from_user.first: {} rom_user.last_name: {}'\
         .format(message.message_id, message.chat.id, message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    await bot.send_message(message.from_user.id, ms)

    await bot.send_message(message.from_user.id, 'Сообщение 1. Введите 1 или 2')
    State.flag = 1
    print(message)


@dp.message_handler(lambda message: message.text == '1' and State.flag == 1 )
async def mes2(message: types.Message):
    await bot.send_message(message.from_user.id, 'Сообщение 2. Введите 1 или 2')
    State.flag = 2

@dp.message_handler(lambda message: message.text == '1' and State.flag == 2 )
async def mes4(message: types.Message):
    await bot.send_message(message.from_user.id, 'Сообщение 4. Введите /start')
    State.flag = 4

@dp.message_handler(lambda message: message.text == '2' and State.flag == 2 )
async def mes4(message: types.Message):
    await bot.send_message(message.from_user.id, 'Сообщение 5. Подождите 10 секунд.')
    await asyncio.sleep(10)
    await bot.send_message(message.from_user.id, 'Сообщение 7. Введите /start')
    State.flag = 7




@dp.message_handler(lambda message: message.text == '2' and State.flag == 1 )
async def mes3(message: types.Message):
    await bot.send_message(message.from_user.id, 'Сообщение 3. Введите номер телефона')
    State.flag = 3

@dp.message_handler(lambda message: State.flag == 3 )
async def mes3(message: types.Message):
    await bot.send_message(message.from_user.id, 'Сообщение 6. Введите /start')
    State.flag = 6


executor.start_polling(dp)













    
"""

@dp.message_handler(lambda message: message.text == '111' )
async def fun1(message: types.Message):
    ms = 'ms'
    await bot.send_message(message.from_user.id, ms)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    argument = message.get_args()
    print(argument)
    print(message.from_user)
    print(message.chat)
    print(message.chat.id)
    print(message.chat.title)
    print(message.sender_chat)
    await message.reply("Привет!\nНапиши мне что-нибудь!")



@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    #await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")
    ms = 'message_id: {} chat.id: {} from_user.id: {} from_user.username: {} from_user.first: {} rom_user.last_name: {}'\
         .format(message.message_id, message.chat.id, message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    await bot.send_message(message.from_user.id, ms)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

        
"""



