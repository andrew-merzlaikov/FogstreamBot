from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserTelegram
from appadmin.models import (Sequence_Logic,
                            User_Sequence_Logic,
                            Message,
                            Question, 
                            AnswerUser)
from .serializers import (UserSerializer,
                          AnswerSerializer)
import json
import logging

logger = logging.getLogger(__name__)


class UserView(APIView):

    def post(self, request):
        
        data_user = json.loads(request.data)['user'] 
        serializer = UserSerializer(data=data_user)

        if serializer.is_valid():
            user_saved = serializer.save()
            
            logger.debug("TelegramUser '{user_saved}' " 
                                        "created successfully".\
                                        format(user_saved=user_saved))

            return Response({"success": "TelegramUser '{user_saved}' " 
                                        "создан успешно".\
                                        format(user_saved=user_saved)},
                                        content_type="json\application")
        else:
            logger.debug("Не валидные данные")
            return Response({"error": "Не валидные данные"},
                            content_type="json\application")


class AnswerView(APIView):

    def get(self, request):
        return Response({"count_entities": Sequence_Logic.\
                                            objects.\
                                            count()},
                        content_type="json\application")

    def post(self, request):
        data_answer = json.loads(request.data)['answer'] 
        serializer = AnswerSerializer(data=data_answer)
        
        if serializer.is_valid():
            answer_saved = serializer.save()

            logger.debug("AnswerUsed '{answer_saved}' " 
                                        "created successfully".\
                                        format(answer_saved=answer_saved))

            return Response({"success": "AnswerUser {answer_saved}".\
                                        format(answer_saved=answer_saved)},
                                        content_type="json\application")
        else:      
            print("Не валидные данные")      
            logger.debug("Не валидные данные")
            return Response({"error": "Не валидные данные"})


class LogicApiView(APIView):

    def get(self, request, id_user):

        if not Sequence_Logic.objects.all().exists():
            return Response({"msg": "Логика общения не создана"},
                            content_type="json\application",
                            status=status.HTTP_404_NOT_FOUND)

        if UserTelegram.objects.\
                        filter(id=id_user).\
                        exists():

            if User_Sequence_Logic.objects.\
                                  filter(user_id=id_user).\
                                  exists():
                
                user_squence_logic = User_Sequence_Logic.\
                                     objects.\
                                     filter(
                                            user_id=id_user
                                      ).\
                                     first()

                id_record = user_squence_logic.next_entity(id_user)

                if Sequence_Logic.objects.filter(id=id_record).exists():
                
                    squence_logic = Sequence_Logic.\
                                                objects.\
                                                filter(id=id_record).\
                                                first()
                    
                    message = Message.objects.\
                                            filter(id=squence_logic.message_id).\
                                            first()

                    question = Question.objects.\
                                                filter(id=squence_logic.question_id).\
                                                first()
                    
                    return Response({"message_id": squence_logic.message_id, 
                                    "question_id": squence_logic.question_id
                                    },
                                    content_type="json\application")  
                else:
                    return Response({"msg": "Конец логики"},
                                    content_type="json\application",
                                    status=status.HTTP_404_NOT_FOUND)

            else:   
                squence_logic = Sequence_Logic.objects.first()

                user_telegram = UserTelegram.\
                                objects.\
                                filter(id=id_user).\
                                first()

                squence_logic_user = User_Sequence_Logic.\
                                     objects.\
                                     create(user_id=user_telegram.id,
                                            number_record_logic_id=squence_logic.id)
               
                squence_logic = Sequence_Logic.\
                                objects.\
                                filter(id=squence_logic_user.\
                                      number_record_logic_id).\
                                first()

                message = Message.\
                          objects.\
                          filter(id=squence_logic.message_id).\
                          first()

                question = Question.\
                           objects.\
                           filter(id=squence_logic.question_id).\
                           first()

                return Response({"message_id": squence_logic.message_id, 
                                 "question_id": squence_logic.question_id
                                },
                                content_type="json\application")
        else:
            return Response({"msg": "Нет пользователя с таким id"},
                            content_type="json\application",
                            status=status.HTTP_404_NOT_FOUND)

