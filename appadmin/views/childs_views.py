from django.views.generic.base import TemplateView
from appadmin.models import Message
from appadmin.forms import (CountChildsMessageForm,
                            MessageForm)
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import modelformset_factory
from django.forms import formset_factory


def get_form_edit_childs(request, id_parent):
    """
    Функция которая возвращает таблицу для редактирования
    потомков
    :param id_parent: id родителя
    :type id_parent: int
    :return: возвращает таблицу для редактирования потомков 
    если пользователь авторизован, ошибку иначе
    """
    if request.user.is_authenticated:
        messages = Message.\
                   objects.\
                   filter(id_parent=id_parent).\
                   all()
        
        return render(request, 
                    "logic/edit_childs.html",
                    {"messages": messages})
    else:
        return render(request, "http_response/error_401.html", status=401)


def get_childs_message(request, id_message):
    """
    View который возвращает детей сообщения
    с id=id_messages
    :param id_message: айди сообщения
    :type id_message: int
    :return: возвращает список с детьми сообщения, 
    иначе ошибку авторизации
    """
    if request.user.is_authenticated:
        messages_childs = Message.\
                        objects.\
                        filter(id_parent=id_message).\
                        all()
        
        message = Message.\
                objects.\
                filter(id=id_message).\
                get()

        root = False

        if message.id_parent == 0:
            root = True
        

        return render(request, 
                    "logic/view_childs.html",
                    {"childs": messages_childs,
                    "root": root})
    else:
        return render(request, "http_response/error_401.html", status=401)


class ViewChilds(TemplateView):
    def get(self, request, id_parent):
        """
        Возвращает формы для создания потомков
        :param id_parent: id родителя
        :type id_parent: int
        :return: возвращает формы для создания потомков
        если пользователь авторизован, иначе ошибка
        """
        if request.user.is_authenticated:
            
            childs = Message.\
                     objects.\
                     filter(id_parent=id_parent).\
                     all()

            for child in childs:
                print(child)

            message = Message.\
                    objects.\
                    filter(id=id_parent).\
                    get()
                

            count_childs = int(request.GET.get('count_childs', 0))
            
            count_childs_form = CountChildsMessageForm(
                                            initial={
                                            'count_childs':count_childs
                                            })

            form_set_childs = formset_factory(MessageForm,
                                              extra=count_childs)

            return render(request, 
                        "logic/create_childs.html" ,
                        {"message": message,
                        "count_childs_form": count_childs_form,
                        "form_set_childs": form_set_childs,
                        "count_childs": count_childs,
                        "childs": childs})
        
        else:
            return render(request, "http_response/error_401.html", status=401)
        
    def post(self, request, id_parent, count_childs):
        """
        Устанавливает потомков для родительского сообщения
        с id=id_parent
        :param id_parent: id родителя
        :type id_parent: int
        :param count_childs: количество потомков
        :type count_childs: int
        :return: возвращается на форму создания потомков если
        пользователь авторизован, иначе выводит ошибку
        """

        if request.user.is_authenticated:
            count_childs = int(count_childs)
            MessageFormSet = formset_factory(MessageForm, 
                                            extra=count_childs)
            
            formset = MessageFormSet(request.POST)

            if formset.is_valid():
                for form in formset: 
                    text_message = form.cleaned_data['text_message']
                    write_answer = form.cleaned_data['write_answer']
                    display_condition = form.cleaned_data['display_condition']
                    display_condition = display_condition.lower()

                    if display_condition == '':
                        display_condition = None


                    Message.objects.create(text_message=text_message,
                                           write_answer=write_answer,
                                           id_parent=id_parent,
                                           display_condition=display_condition)

            url_for_redirect = reverse('appadmin:get_form_create_childs',
                                       kwargs={'id_parent':id_parent})

            url_for_redirect += ('?count_childs=' + count_childs)

            return HttpResponseRedirect(url_for_redirect)

        else:
            return render(request, "http_response/error_401.html", status=401)
