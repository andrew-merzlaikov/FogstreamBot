# FogstreamBot
Бизнес-кейс telegram-бота

Проект состоит из двух частей: сервер и бот  
Appadmin - приложение для админ-панели  
Appserver - приложение для REST API  

1) Создать папку где будет храниться проект и перейти в нее  
2) Нужно перейти в эту папку и склонировать туда репозиторий
   git clone https://github.com/DanilMazurkin/FogstreamBot.git FogstreamBot  
3) Создать виртуальную среду python3 -m venv <имя_виртуальной_среды>  
4) В конечном счете структура папок должна быть следующей  
![alt tag](https://github.com/DanilMazurkin/FogstreamBot/blob/main/readme_screen/1.png)
6) Перейти в нее source <имя_виртуальной_среды>/bin/activate
7) Установить django командой pip install django  
8) сd FogstreamBot
9) Установить все зависимости pip install -r requirements.txt  

Запуск сервера

Перед запуском сервера надо установить переменные окружения

Переменные окружения для сервера:  
DBNAME=<имя_базы_данных>  
DBUSER=<имя_пользователя_данных>  
PASS=<пароль_базы_данных>  
HOST=<хост_сервера>  

9) Перейти в папку FogstreamBot  
10) Создать миграции python manage.py makemigrations  
11) Применить миграции python manage.py migrate  

12) Создать суперпользователя в консоле django со своими параметрами
13) python manage.py runserver  
14) Перейти в браузере по ссылке 127.0.0.1:8000/bot/login

Запуск бота

Перед запуском бота необходимо запустить сервер
-----

1. source name_env/bin/activate  
2. Необходимо запустить бота  
   cd telegrambot  
   python bothandlers.py  

Перед запуском бота надо установить следующие переменные окружения

PORT_SERVER=<порт_запущенного_сервера>  
HOST=<хост_запущенного_сервера>  

