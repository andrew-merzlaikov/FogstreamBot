from django.db import models


class TokenBot(models.Model):
    """
    Модель для представления токена в БД
    token_bot - токен бота
    """
    token_bot = models.CharField(max_length=500)

    def __str__(self):
        """
        Представления токена
        """
        return "{token_bot}".format(token_bot=self.token_bot)


class Message(models.Model):
    """
    Модель для представления сообщения в БД
    text_message - текст сообщения
    id_parent - id родителя
    display_condition - условие отображение (как надо ответить на родительское
    сообщение чтобы это сообщение появилось)
    write_answer - Bool значение которое определяет вопрос ли это
    """
    text_message = models.CharField(max_length=500)

    id_parent = models.IntegerField(null=True)

    display_condition = models.CharField(max_length=50, 
                                         null=True, 
                                         blank=True)

    write_answer = models.BooleanField(blank=True,
                                       null=True)

    def __str__(self):  
        """
        Представление сообщения
        """
        return "{text_message}".format(text_message=self.text_message)


class MessageDelay(models.Model):
    """
    Модель для представления задержек сообщения
    message - связанное поле с моделью Message
    delay - задержка сообщения
    """
    message = models.OneToOneField(Message, 
                                   on_delete=models.CASCADE, 
                                   primary_key=True)
    delay = models.IntegerField()


class UserTelegram(models.Model):
    """
    Модель для представления пользователя телеграм
    first_name - имя пользователя
    last_name - фамилия пользователя
    username - никнейм пользователя
    id_user_telegram - id пользователя telegram
    current_message - id текущего сообщения
    """
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=30, default=None)
    username = models.CharField(max_length=30, default=None)
    id_user_telegram = models.IntegerField(primary_key=True)

    current_message =  models.ForeignKey(Message, 
                                         on_delete=models.CASCADE, 
                                         default=None)

    first_name.null = True
    last_name.null = True
    username.null = True
    current_message.null = True

    def __str__(self):
        """ Представления для отображения UserTelegram """
       
        return "{first_name} {last_name} {username} ".\
                format(username=self.username,
                       first_name=self.first_name,
                       last_name=self.last_name)


class AnswerUser(models.Model):
    """
    Модель для представления ответов пользователя 
    на сообщения
    telegram_user - поле связанное с моделью TelegramUser из
    appserver
    message - поле связанное с моделью Message
    answer - ответ пользователя на вопрос
    """
    telegram_user = models.ForeignKey(UserTelegram, 
                                      on_delete=models.\
                                                CASCADE)
    
    message = models.ForeignKey(Message,
                                on_delete=models.\
                                          CASCADE)
    
    answer = models.CharField(max_length=100)