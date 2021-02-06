# FogstreamBot
Бизнес-кейс telegram-бота
1. git clone https://github.com/DanilMazurkin/FogstreamBot.git  
2. Создать виртуальную среду python3 -m venv name_env  
3. source name_env/bin/activate  
4. Для работы с базой данных PostgreSQL  
   надо установить переменные окружения, где:  
   DBNAME = <имя_базы_данных>  
   DBUSER = <имя_пользователя>  
   PASS = <пароль_от_БД>  
   HOST = <хост_БД>  
5. pip install django  
6. pip install djangorestframework  
7. Запустить тестовый сервер python manage.py runserver your_server_ip:8000
