import requests
import json
import os


class BotServer:

    def __init__(self):
        self.url_host = os.environ.get('HOST')
        self.url_port = os.environ.get('PORT_SERVER')
        self.url_for_users = ("http://" + self.url_host + 
                              ':' + self.url_port + '/api/users')
        self.url_for_answer_with_user = ("http://" + self.url_host + ':' + 
                                         self.url_port + '/api/set/answer')

    def create_user_in_server(self, name, lastname, username):

        data_for_create_user = {
            "user": {
                "first_name": name,
                "last_name": lastname,
                "username": username
            }
        }

        requests.post(self.url_for_users, json=json.dumps(data_for_create_user))
    
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