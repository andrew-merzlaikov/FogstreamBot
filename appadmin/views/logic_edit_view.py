from django.views.generic.base import TemplateView
from appadmin.models import Message
from appadmin.forms import MessageForm
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import modelformset_factory
from django.forms import formset_factory
from django import forms


def get_table_for_logic(request):
    """
    Возвращает таблицу в которой можно 
    просмотреть логику если пользователь
    авторизован, иначе вернет ошибку
    """
    if request.user.is_authenticated:

        messages = Message.objects.all()
        
        return render(request,
                    "logic/view_logic.html",
                    {"messages": messages})
    else:
        return render(request, "http_response/error_401.html", status=401)

def get_form_create_logic(request):
    """
    Возвращает таблицу через которую
    можно создать потомков для сообщения
    если пользователь авторизован иначе
    возвращает ошибку
    """
    if request.user.is_authenticated:
        messages = Message.objects.all()
        exists_logic = Message.\
                    objects.\
                    first()

        message_form = MessageForm()

        return render(request, 
                    "logic/create_logic.html",
                    {"messages": messages, 
                    "exists_logic": exists_logic,
                    "form": message_form})
    else:
        return render(request, "http_response/error_401.html", status=401)

def delete_logic(request):
    """
    Удаляет логику общения бота если пользователь
    авторизован иначе вернет ошибку
    """
    if request.user.is_authenticated:
        all_messages = Message.objects.all()

        for message in all_messages:
            message.delete()

        url_for_redirect = reverse("appadmin:get_create_logic")
        params_delete = "?delete_logic=True"

        url_for_redirect = url_for_redirect + params_delete

        return HttpResponseRedirect(url_for_redirect)
    else:
        return render(request, "http_response/error_401.html", status=401)