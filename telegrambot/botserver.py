import requests
import json
import os
from django.db.models import Q


class BotServer:
    """
    В этом классе описаны функции, которые делают
    запросы к API сервера на Django
    """


    def __init__(self):
        self.url_host = os.environ.get('HOST')
        self.url_port = os.environ.get('PORT_SERVER')
        
        self.url_for_users = ("http://" + self.url_host + 
                              ':' + self.url_port + '/api/users')
        self.url_for_root_message = ("http://" + self.url_host + 
                                    ':' + self.url_port + '/api/get/root/message')

        self.url_for_next_message = ("http://" + self.url_host + 
                                    ':' + self.url_port + '/api/get/next/message/')
        
        self.url_for_options_answers = ("http://" + self.url_host + ':' +
                                        self.url_port + '/api/get/options_answers/')

        self.url_for_check_end_tree = ("http://" + self.url_host + ':' +
                                        self.url_port + '/api/get/check/end_tree/')

        self.url_for_get_token = ("http://" + self.url_host + ':' +
                                  self.url_port + '/api/get/token') 
        self.url_for_get_delay = ("http://" + self.url_host + ':' +
                                  self.url_port + '/api/get/delay/message/') 

    def get_delay_message(self, id_message):
        """
        Функция которая возвращает задержку для сообщения
        с id=id_message
        Если для сообщения не установлена задержка, то вернет -1
        """

        url_for_get_delay = self.url_for_get_delay + str(id_message)

        r = requests.get(url_for_get_delay)

        return r.json()['delay']

    def get_options_answers(self, id_current_message):
        """
        Функция которая возвращает
        варианты ответа для сообщения с id=id_current_message
        """

        url_for_option = self.url_for_options_answers + str(id_current_message)

        r = requests.get(url_for_option)

        return r.json()

    def get_token(self):
        """
        Функция которая возвращает токен бота
        """
        r = requests.get(self.url_for_get_token)

        return r.json()

    def get_check_end_tree(self, id_current_message):
        """
        Функция которая проверяет является ли сообщение 
        с id=id_current_message последним в дереве
        """
        url_for_check = self.url_for_check_end_tree + str(id_current_message)

        r = requests.get(url_for_check)

        return r.json()["exists"]

    def get_root_message(self): 
        """
        Функция которая возвращает корневое сообщение
        """
        r = requests.get(self.url_for_root_message)
        
        return r.json()

    def get_next_message(self, id_current_message, answer = None):
        """
        Функция которая получает следующее сообщение
        """
        url_for_next_message = None

        if answer is not None:
            url_for_next_message = (self.url_for_next_message + str(id_current_message) + 
                                   '?answer=' + answer)
        else:
            url_for_next_message = self.url_for_next_message + str(id_current_message)


        r = requests.get(url_for_next_message)
        
        return r.json()

    def create_user_in_server(self, user_id, name, lastname, username):
        """
        Функция которая создает пользователя на сервере
        """

        data_for_create_user = {
            "user": {
                "first_name": name,
                "last_name": lastname,
                "username": username,
                "id_user_telegram": user_id
            }
        }

        r = requests.post(self.url_for_users, json=data_for_create_user)
        

        return r.json()

  