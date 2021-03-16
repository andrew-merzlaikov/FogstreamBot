import logging

class BotFlag:
    """
    Класс предназначен для работы с флагами
    Флаг устанавливается для каждого состояния
    """
    def __init__(self):
        """
        Инициализирует словарь в котором хранится информация 
        о установленном флаге для каждого пользователя
        """
        self.dict_with_user = dict()

    def set_flag_user(self, message_chat_id, flag):
        """
        Устанавливается flag по чат id
        """
        self.dict_with_user[message_chat_id] = flag

    def get_flag_user(self, message_chat_id):
        """
        Получает flag по чат id
        """
        return self.dict_with_user[message_chat_id]