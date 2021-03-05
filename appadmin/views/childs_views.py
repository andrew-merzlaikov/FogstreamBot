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


def get_childs_message(request, id_message):
    """
    View который возвращает детей сообщения
    с id=id_messages
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
        """
        if request.user.is_authenticated:
            count_childs_form = CountChildsMessageForm()
            
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

                    if display_condition == '':
                        display_condition = None

                    Message.objects.create(text_message=text_message,
                                        write_answer=write_answer,
                                        id_parent=id_parent,
                                        display_condition=display_condition)

            return HttpResponseRedirect(reverse('appadmin:get_form_create_childs',
                                                kwargs={'id_parent':id_parent}))

        else:
            return render(request, "http_response/error_401.html", status=401)
