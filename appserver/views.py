from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from .serializers import UserSerializer
from appadmin.models import (Message,
                             TokenBot,
                             MessageDelay,
                             AnswerUser,
                             UserTelegram)
from .serializers import UserSerializer
from django.db.models import Q
import json
import logging
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


@api_view(('GET', ))
def get_current_message(request, id_user_telegram):
    """
    Эндпоинт который возвращает текущее сообщение в базе данных
    :param id_user_telegram: айди пользователя telegram в базе
    Возвращает сообщение со всеми его полями
    """
    user_telegram  = UserTelegram.\
                        objects.\
                        filter(id_user_telegram=id_user_telegram).\
                        get()


    return Response({"message": {
                        "id": user_telegram.current_message.id,
                        "text_message": user_telegram.current_message.text_message,
                        "id_parent": user_telegram.current_message.id_parent,
                        "display_condition": user_telegram.current_message.display_condition,
                        "write_answer": user_telegram.current_message.write_answer
                    }
                    },
                     content_type="json\application")

@api_view(('POST', ))
def set_current_message(request, id_current_message, id_user_telegram):
    """
    Эндпоинт который устанавливает текущее сообщение в базе данных 
    :param id_current_message: айди текущего сообщения
    :param id_user_telegram: уникальный айди пользователя в телеграме
    Возвращает айди пользователя если пользователь существует в базе данных, 
    иначе выдает ошибку
    """
    user_telegram_exists = UserTelegram.\
                            objects.\
                            filter(id_user_telegram=id_user_telegram).\
                            exists()

    if user_telegram_exists:

        user_telegram = UserTelegram.\
                        objects.\
                        filter(id_user_telegram=id_user_telegram).\
                        get()

        if id_current_message == 0:
            msg = Message.\
                  objects.\
                  filter(id_parent=0).\
                  get()

            user_telegram.current_message = msg
            user_telegram.save()
        else:
            msg = Message.\
                  objects.\
                  filter(id=id_current_message).\
                  first()

            user_telegram.current_message = msg
            user_telegram.save()

        return Response({"id_current_message": id_current_message},
                        content_type="json\application")
   
    else:
        return Response({"error": "Пользователь не существует"},
                        content_type="json\application")

@api_view(('GET', ))
def get_delay_for_message(request, id_message):
    """
    Функция возвращает задержку для сообщения
    с id=id_message
    :param id_message: id сообщения
    :return: Возвращает объект Response JSON 
    с задержкой сообщения если задержка на сообщение задана,
    иначе возвращает 0
    :rtype: Response
    """

    exists_delay = MessageDelay.\
                   objects.\
                   filter(message_id=id_message).\
                   exists()

    if exists_delay:
        message = MessageDelay.\
                  objects.\
                  filter(message_id=id_message).\
                  get()

        return Response({"delay": message.delay},
                        content_type="json\application")
    else:
        return Response({"delay": 0}, 
                        content_type="json\application")

@api_view(('GET', ))
def count_childs(request, id_current_message):
    """
    Эндпоинт возвращает количество 
    потомков для сообщения с id=id_current_message
    :param id_current_message: id текущего сообщения
    :return: Возвращает Response JSON объект, где
    count - задержка сообщения
    :rtype: Response
    """
    count = Message.\
            objects.\
            filter(id_parent=id_current_message).\
            count()
    
    return Response({"count": count}, 
                    content_type="json\application")

@api_view(('POST', ))
def set_answer_user(request, id_user_telegram):
    """
    Эндпоинт устанавливает ответ на вопрос 
    пользователя с message.from_user.id=id_user_telegram
    :param id_user_telegram: id пользователя в telegram
    :type id_user_telegram: string
    :return: Возвращает {"status": True} true
    :rtype: Response
    """   
    answer = request.POST['answer']
    id_message = request.POST['id_message']
    
    answer = AnswerUser.\
             objects.\
             update_or_create(telegram_user_id=id_user_telegram,
                              message_id=id_message, 
                              defaults={
                                "answer": answer
                              })
    
                              
    return Response({"status": True}, 
                    content_type="json\application")

@api_view(('GET', ))
def get_options_answers(request, id_current_message):
    """
    Эндпоинт возвращает ответы на сообщение
    с id=id_current_message
    :param id_current_message: id текущего сообщения
    :type id_current_message: int
    :return: Если варианты ответа на сообщение
    есть, то возвращается список с вариантами ответа в 
    виде Response JSON {"options_answer": options_answer},
    иначе пользователю вернется None
    :rtype: Response JSON
    """
    messages = Message.\
                      objects.\
                      filter(id_parent=id_current_message).\
                      all()
    
    options_answer = list()

    for message in messages:
        if message is not None:
            if message.display_condition is not None:
                options_answer.append(message.display_condition)
    
    options_answer = sorted(options_answer)

    if options_answer:
        return Response({"options_answer": options_answer},
                        content_type="json\application")
    else:
        return Response({"options_answer": None},
                        content_type="json\application")

@api_view(('GET', ))
def get_token_bot(request):
    """
    Возвращает токен бота, который установил пользователь
    через админку
    :return: Возвращает токен бота в следующем виде
    {"token": str(token)}
    :rtype: Response JSON
    """
    token = TokenBot.objects.first()

    return Response({"token": str(token)}, 
                    content_type="json\application")


class UserView(APIView):
    """
    CBV который описывает пользователя Telegram
    """
    def post(self, request):   
        """
        Создает пользователя telegram в БД
        """     
        data_user = request.data['user'] 
        serializer = UserSerializer(data=data_user)

        if serializer.is_valid():
            id_user_telegram = data_user['id_user_telegram']

            msg = Message.\
                  objects.\
                  filter(id_parent=0).\
                  get()

            user_saved = serializer.save()
            user_telegram = UserTelegram.\
                                objects.\
                                filter(id_user_telegram=id_user_telegram).\
                                get()
                
            user_telegram.id_current_message = msg
            user_telegram.save()

            return Response({"success": "TelegramUser '{user_saved}' " 
                                            "создан успешно".\
                                            format(user_saved=user_saved),
                             "text_message": user_telegram.id_current_message.text_message},
                             content_type="json\application")
        else:
                        
            return Response({"error": "Не валидные данные"},
                            content_type="json\application")


class MessageView(APIView):
    """
    CBV который описывает сообщения
    """

    def get(self, request, id_current_message = 0):
        """
        Возвращает сообщение с базы данных
        В эндпоинт также GET параметром может передаваться
        answer - это ответ на текущее собщение
        :param id_current_message: id текущего сообщения
        :type id_current_message: int
        :return: Возвращает Response JSON объект
        со следующими полями
        {
        "message": {
            "id": message.id,
            "text_message": message.text_message,
            "id_parent": message.id_parent,
            "display_condition": message.display_condition,
            "write_answer": message.write_answer
        }},
        id - id сообщения
        text_message - текст сообщения
        id_parent - id родителя
        display_condition - условие отображения
        write_answer - Bool значение, которое отвечает надо ли
        писать ответ на вопрос
        """
        answer = None
        message = None


        if id_current_message == 0:
            message = Message.\
                      objects.\
                      filter(id_parent=0).\
                      get()

            return Response({"message": {
                                "id": message.id,
                                "text_message": message.text_message,
                                "id_parent": message.id_parent,
                                "display_condition": message.display_condition,
                                "write_answer": message.write_answer
                            }}, content_type="json\application") 

        if 'answer' in request.GET.keys():
            answer = request.GET['answer']


        if answer is not None:
        

            message = Message.\
                    objects.\
                    filter(id_parent=id_current_message).\
                    all()
            

            if message[0].display_condition is not None:

                message = Message.\
                          objects.\
                          filter(id_parent=id_current_message).\
                          filter(display_condition=answer).\
                          get()
                
                print(message)
            else:
                message = Message.\
                          objects.\
                          filter(id_parent=id_current_message).\
                          get()

        else:
            message = Message.\
                      objects.\
                      filter(id_parent=id_current_message).\
                      get()

        return Response({"message": {
                            "id": message.id,
                            "text_message": message.text_message,
                            "id_parent": message.id_parent,
                            "display_condition": message.display_condition,
                            "write_answer": message.write_answer
                        }}, content_type="json\application") 

