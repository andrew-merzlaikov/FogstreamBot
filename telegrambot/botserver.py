import requests
import json
import os
from django.db.models import Q


class BotServer:

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

    def get_options_answers(self, id_current_message):

        url_for_option = self.url_for_options_answers + str(id_current_message)

        print("URL: " + url_for_option)

        r = requests.get(url_for_option)

        return r.json()

    def get_check_end_tree(self, id_current_message):
        url_for_check = self.url_for_check_end_tree + str(id_current_message)

        r = requests.get(url_for_check)

        return r.json()["exists"]

    def get_root_message(self): 
        r = requests.get(self.url_for_root_message)
        
        return r.json()

    def get_next_message(self, id_current_message, answer = None):
        url_for_next_message = None

        if answer is not None:
            url_for_next_message = (self.url_for_next_message + str(id_current_message) + 
                                   '?answer=' + answer)
        else:
            url_for_next_message = self.url_for_next_message + str(id_current_message)


        r = requests.get(url_for_next_message)
        
        return r.json()

    def create_user_in_server(self, user_id, name, lastname, username):


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

  