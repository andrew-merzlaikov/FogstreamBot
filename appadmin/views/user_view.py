from django.views.generic.base import TemplateView
from appserver.models import UserTelegram
from django.shortcuts import render
from appadmin.models import AnswerUser


def get_info_user(request, telegram_user_id):
    """
    Возвращает ответы пользователей на вопросы
    """

    if request.user.is_authenticated:
        answers = AnswerUser.\
                    objects.\
                    filter(telegram_user_id=telegram_user_id).\
                    all()

        return render(request, "answers/answer.html", {"answers": answers})
    else:
        return render(request, "http_response/error_401.html", status=401)

def info_users_list(request):
    """
    Возвращает список пользовтелей для администратора
    """
    if request.user.is_authenticated:
        users_telegram = UserTelegram.\
                         objects.\
                         all()

        return render(request, 
                      "users/info_users.html", 
                      {"users": users_telegram})
    else:
        return render(request, "http_response/error_401.html", status=401)
