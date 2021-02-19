# FogstreamBot
Бизнес-кейс telegram-бота

Проект состоит из двух частей: сервер и бот  

Нужно склонировать репозиторий к себе на ПК   
git clone https://github.com/DanilMazurkin/FogstreamBot.git  

cd FogstreamBot

Создать виртуальную среду python3 -m venv <имя_виртуальной_среды>  

Перед установкой бота и сервера необходимо  
установить пакеты командой: pip install -r requirements.txt  

Установка сервера: 

1. cd fogstreambot
2. python manage.py runserver  

Перед установкой переменных окружения: source <имя_виртуальной_среды>/bin/activate  

Переменные окружения для сервера:  
DBNAME=<имя_базы_данных>  
DBUSER=<имя_пользователя_данных>  
PASS=<пароль_базы_данных>  
HOST=<хост_сервера>  

Установка бота

Перед установкой переменных окружения: source <имя_виртуальной_среды>/bin/activate  

Переменные окружения для бота:  
PORT_SERVER=<порт_запущенного_сервера>  
HOST=<хост_сервера>  

1. source name_env/bin/activate  
2. Необходимо запустить бота  
   cd telegrambot  
   python bothandlers.py  
