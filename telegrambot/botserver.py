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

        self.url_for_set_answer = ("http://" + self.url_host + ':' +
                                   self.url_port + '/api/set/answer/')

    def set_answer_user(self, user_id_telegram, message_id, answer):
        """
        Функция которая устанавливает ответ пользователя в Базе данных
        :param user_id_telegram: Уникальный id для пользователя telegram
        :param message_id: Id сообщения на который устанавливается ответ
        :param answer: Текст ответа
        """
        
        url_for_request = self.url_for_set_answer + str(user_id_telegram)

        data_for_set = {
            "id_message": message_id,
            "answer": answer
        }

        print("Функция для сохранения ответа")

        requests.post(url_for_request, data=data_for_set)

    def get_delay_message(self, id_message = 0):
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

    def get_next_message(self, id_current_message = None, answer = None):
        """
        Функция которая получает следующее сообщение
        Если id_current_message = None, то будем получать корневое
        сообщение
        """
        url_for_next_message = None
    
        if id_current_message is None:
            url_for_next_message = (self.url_for_next_message + '0')
            print("URL: ", url_for_next_message)
        elif answer is not None:
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

    def get_next_fullmessage(self, id_current_message = None, answer = None):
        """ 
        Возврашает словарик в следующем виде:
        {'id': 61, 
        'text_message': 'Вы можете получить информацию из следующих источников\r\n1 - instagram.com\r\n2 - vk.com\r\n3 - telegram', 
        'id_parent': 58, 
        'display_condition': 'Да', 
        'write_answer': True, 
        'delay': 900, 
        'options_answer': ['2', '1', '3']}

        delay - задержка этого сообщения
        options_answer - варианты ответа на сообщение
        (если вариантов нет, то None)
        id - id_сообщения,
        text_message - текст сообщения
        write_answer - Вопрос ли это (надо ли отвечать на этот вопрос)
        display_condition - Условие отображения

        """
        
        r_delay = None
        r_message = self.get_next_message(id_current_message, answer)

        if id_current_message is None:
            r_delay = self.get_delay_message(r_message["message"]["id"])
        else:
            r_delay = self.get_delay_message(id_current_message)
        
        r_options = self.get_options_answers(r_message["message"]["id"])

        result_dict = r_message["message"]
        result_dict["delay"] = r_delay
        result_dict["options_answer"] = r_options["options_answer"]

        print(result_dict)

        return result_dict

        