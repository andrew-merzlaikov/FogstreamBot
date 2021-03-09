class BotFlag:

    def __init__(self):
        self.dict_with_user = dict()

    def set_flag_user(self, message_chat_id, flag):
        self.dict_with_user[message_chat_id] = flag

    def get_flag_user(self, message_chat_id):
        return self.dict_with_user[message_chat_id]