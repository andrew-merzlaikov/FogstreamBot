from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserTelegram
import json
from .serializers import UserSerializer

# from appadmin.models import (Sequence_Logic,
#                             User_Sequence_Logic,
#                             Message,
#                             Question, 
#                             AnswerUser)
# from .serializers import (UserSerializer,
#                           AnswerSerializer)
# from django.db.models import Q
# import json
# import logging
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


# logger = logging.getLogger(__name__)

# @api_view(['GET',])
# def get_logic_entity(request):
#     if request.method == "GET":
#         return Response({"count": Sequence_Logic.\
#                                             objects.\
#                                             count()},
#                         content_type="json\application")

# @api_view(['GET',])
# def get_current_entity(request, id_user):
#     if request.method == "GET":
        
#         if not User_Sequence_Logic.objects.\
#                                    filter(user=id_user).\
#                                    exists():
#             return Response({'error': 'Нет сущности!'},
#                             content_type="json\application",
#                             status=status.HTTP_404_NOT_FOUND)
        
        
        
#         logic = User_Sequence_Logic.objects.\
#                                       get(user=id_user).\
#                                       number_record_logic


#         if logic.message_id is not None:
#             message = Message.objects.filter(id=logic.message_id).get()
            
#             return Response({"type": "message",
#                              'message': message.text_message,
#                             }, content_type="json\application")

        
#         if logic.question_id is not None:
#             question = Question.objects.filter(id=logic.question_id).get()

#             text = question.question
            
#             confirm_text = question.question_confirm 

#             confirm_not_text = question.question_not_confirm 

#             return Response({"type": "question",
#                              'question_text': text,
#                              'confirm': confirm_text,
#                              'not_confirm': confirm_not_text
#                             }, content_type="json\application")

class UserView(APIView):

    def get(self, request):
        
        name = self.request.GET.get('name')
        lastname = self.request.GET.get('lastname')
        username = self.request.GET.get('username')

        if name is None:
            name = ""
        if lastname is None:
            lastname = ""
        if username is None:
            username = ""

        criter_username = Q(username__icontains=username)
        criter_first_name = Q(first_name__icontains=name)
        criter_last_name = Q(last_name__icontains=lastname)

        user_exists = UserTelegram.\
                                    objects.\
                                    filter(criter_username &
                                           criter_first_name &
                                           criter_last_name).\
                                    exists()

        if user_exists:
            
            user = UserTelegram.\
                            objects.\
                            filter(criter_username &
                                   criter_first_name &
                                   criter_last_name).\
                            get()

            return  Response({"id_user": user.id},
                             content_type="json\application")
        else:
            return  Response({"error": "Не найден пользователь"},
                             content_type="json\application")

    def post(self, request):        
        data_user = request.data['user'] 
        serializer = UserSerializer(data=data_user)

        if serializer.is_valid():
            user_saved = serializer.save()
            
            return Response({"success": "TelegramUser '{user_saved}' " 
                                        "создан успешно".\
                                        format(user_saved=user_saved)},
                                        content_type="json\application")
        else:
                        
            return Response({"error": "Не валидные данные"},
                            content_type="json\application")


# class AnswerView(APIView):

#     def post(self, request):
#         data_answer = json.loads(request.data)['answer'] 
#         serializer = AnswerSerializer(data=data_answer)
        
#         if serializer.is_valid():
#             answer_saved = serializer.save()

#             logger.debug("AnswerUsed '{answer_saved}' " 
#                                         "created successfully".\
#                                         format(answer_saved=answer_saved))

#             return Response({"success": "AnswerUser {answer_saved}".\
#                                         format(answer_saved=answer_saved)},
#                                         content_type="json\application")
#         else:      
#             logger.debug("Не валидные данные")
#             return Response({"error": "Не валидные данные"})


# class LogicApiView(APIView):

#     def get(self, request, id_user):

#         if not Sequence_Logic.objects.all().exists():
#             return Response({"msg": "Логика общения не создана"},
#                             content_type="json\application",
#                             status=status.HTTP_404_NOT_FOUND)

#         if UserTelegram.objects.\
#                         filter(id=int(id_user)).\
#                         exists():

#             if User_Sequence_Logic.objects.\
#                                   filter(user_id=id_user).\
#                                   exists():
                
#                 user_squence_logic = User_Sequence_Logic.\
#                                      objects.\
#                                      filter(
#                                         user_id=id_user
#                                       ).\
#                                      first()

#                 id_record = user_squence_logic.next_entity(id_user)

#                 if Sequence_Logic.objects.filter(id=id_record).exists():
                
#                     squence_logic = Sequence_Logic.\
#                                     objects.\
#                                     filter(id=id_record).\
#                                     first()
                    
#                     message_exists = Message.\
#                                      objects.\
#                                      filter(id=squence_logic.message_id).\
#                                      exists()

#                     question_exists = Question.\
#                                       objects.\
#                                       filter(id=squence_logic.question_id).\
#                                       exists()
                    
#                     if message_exists:
#                         message = Message.\
#                                   objects.\
#                                   filter(id=squence_logic.message_id).\
#                                   get()
                        
#                         return Response({"type": "message",
#                                         "message_text": str(message)},
#                                         content_type="json\application")
                    
#                     elif question_exists:
#                         que = Question.\
#                               objects.\
#                               filter(id=squence_logic.question_id).\
#                               get()

#                         text = que.question
#                         confirm = que.question_confirm
#                         not_confirm = que.question_not_confirm

#                         return Response({"type": "question",
#                                         "question_text": text,
#                                         "confirm_text": confirm,
#                                         "not_confirm_text": not_confirm
#                                         },
#                                         content_type="json\application")
                    
#                 else:
#                     return Response({"msg": "Конец логики"},
#                                     content_type="json\application",
#                                     status=status.HTTP_404_NOT_FOUND)

#             else:   
#                 squence_logic = Sequence_Logic.objects.first()

#                 user_telegram = UserTelegram.\
#                                 objects.\
#                                 filter(id=id_user).\
#                                 first()

#                 squence_logic_user = User_Sequence_Logic.\
#                                      objects.\
#                                      create(user_id=user_telegram.id,
#                                             number_record_logic_id=squence_logic.id)
               
#                 squence_logic = Sequence_Logic.\
#                                 objects.\
#                                 filter(id=squence_logic_user.\
#                                       number_record_logic_id).\
#                                 first()

#                 message_exists = Message.\
#                                 objects.\
#                                 filter(id=squence_logic.message_id).\
#                                 exists()

#                 question_exists = Question.\
#                                 objects.\
#                                 filter(id=squence_logic.question_id).\
#                                 exists()

#                 if message_exists:
#                     message = Message.objects.\
#                                       filter(id=squence_logic.message_id).\
#                                       get()
                    
#                     return Response({"type": "message",
#                                      "message_text": str(message)},
#                                     content_type="json\application")
                
#                 elif question_exists:
#                     question = Question.objects.\
#                                       filter(id=squence_logic.question_id).\
#                                       get()
                    
#                     text = question.question
#                     confirm = question.question_confirm
#                     not_confirm = question.question_not_confirm

#                     return Response({"type": "question",
#                                     "question_text": text,
#                                     "confirm_text": confirm,
#                                     "not_confirm_text": not_confirm
#                                     },
#                                     content_type="json\application")
#         else:
#             return Response({"msg": "Нет пользователя с таким id"},
#                             content_type="json\application",
#                             status=status.HTTP_404_NOT_FOUND)

