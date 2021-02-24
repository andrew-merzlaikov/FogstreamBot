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
        self.url_for_answer_with_user = ("http://" + self.url_host + ':' + 
                                         self.url_port + '/api/set/answer')
        self.url_for_get_id_user = ("http://" + self.url_host + ':' + 
                                         self.url_port + '/api/get/user_id/')
        self.url_for_get_count = ("http://" + self.url_host + ':' + 
                                         self.url_port + '/api/get/count_entities')
        self.url_for_get_entity = ("http://" + self.url_host + ':' + 
                                         self.url_port + '/api/get/next/entity/')
        self.url_for_current_entity = ("http://" + self.url_host + ':' + 
                                                   self.url_port + '/api/get/current/entity/')

    def telegram_user_id_from_database(self, 
                                           username, 
                                           first_name, 
                                           last_name):
        
        params_user = {
            "username": username,
            "name": first_name,
            "lastname": last_name
        }
        
        r = requests.get(self.url_for_get_id_user, 
                        params=params_user)
        
        if "id_user" in r.json().keys():
            return int(r.json()["id_user"])
        else:
            return r.json()["error"]

    def get_logic_entity(self, id_user):        
        url_for_get_entity_with_id = self.url_for_get_entity + str(id_user)
        r = requests.get(url_for_get_entity_with_id)
        
        return r.json()

    def get_count_logic_entities(self):

        r = requests.get(self.url_for_get_count)

        return r.json()["count"]
    
    def create_user_in_server(self, name, lastname, username):

        if name == None:
            name = "NULL"
        
        if lastname == None:
            lastname = "NULL"
        
        if username == None:
            username = "NULL"


        data_for_create_user = {
            "user": {
                "first_name": name,
                "last_name": lastname,
                "username": username
            }
        }

        requests.post(self.url_for_users, json=json.dumps(data_for_create_user))

    def get_current_entity(self, id_user):
        url_for_current_entity = self.url_for_current_entity + str(id_user)
        r = requests.get(url_for_current_entity)

        return r.json()

    def create_answer_with_user(self, answer_text, question_id, user_id):

        data_for_create_answer = {
            "answer": {
                "answer_text": answer_text,
                "question_id": question_id,
                "user_id": user_id
            }
        }

        requests.post(self.url_for_answer_with_user, 
                     json=json.dumps(data_for_create_answer))