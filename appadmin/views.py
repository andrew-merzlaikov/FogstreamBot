from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect
from .models import Message
from .forms import MessageForm
from django.urls import reverse
from appserver.models import UserTelegram
import operator


def show_edit_form_message(request, id_message):
    if request.user.is_authenticated:
        message_form = MessageForm()
        return render(request, 
                      "messages/edit_message.html", 
                      {'message_form': message_form,
                       'id_message': id_message})


class ViewMain(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 
                         "main.html")
        else:
            return render(request, "http_response/error_401.html", status=401)


class ViewMessage(TemplateView):

    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ViewMessage, self).dispatch(*args, **kwargs)

    def get(self, request):
        if request.user.is_authenticated:
            message_form = MessageForm()

            all_messages = Message.objects.all()

            print(all_messages)
            return render(request, 
                         "messages/create_message.html",
                         {"form": message_form,
                          "messages": all_messages})
        else:
            return render(request, "http_response/error_401.html", status=401)

    def post(self, request):
        if request.user.is_authenticated:
            message_form = MessageForm(request.POST)
            
            if message_form.is_valid():
                context_data = {
                    "message": message_form.cleaned_data["text_message"]
                }

                Message.objects.create(text_message=context_data['message'])

                return redirect('/bot/create/message?' + 'status_msg=OK')
            else:
                return render(request, 
                              "http_response/error_422.html", 
                              status=422)

        else:
            return render(request, "http_response/error_401.html", status=401)

    def put(self, request, id_message):
        if request.user.is_authenticated:
            form = MessageForm(request.POST or None)
            print("PUT QUERY MESSAGE")

            if form.is_valid():
                text_message = form.cleaned_data.get("text_message")
                
                Message.\
                        objects.\
                        filter(id=id_message).\
                        update(text_message=text_message)

                return redirect('/bot/create/message?msg_edit=OK')
            else:
                return render(request, 
                              "http_response/error_422.html", 
                              status=422)

        else:
            return render(request, "http_response/error_401.html", status=401)

    def delete(self, request, id_message):
        if request.user.is_authenticated:
            
            Message.\
                    objects.\
                    filter(id=id_message).\
                    delete()
            

            return redirect('/bot/create/message?msg_delete=OK')
        else:
            return render(request, "http_response/error_401.html", status=401)


class ViewUser(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            users_telegrams = UserTelegram.objects.all()

            return render(request, 
                         "users/users.html",
                         {"users_telegram": users_telegrams})
        else:
            return render(request, "http_response/error_401.html", status=401)


class ViewLogic(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            
            all_messages = Message.objects.all()
            MessageFormSet = modelformset_factory(Message, 
                                                  fields=('text_message', 
                                                          'id_parent', 
                                                          'display_condition',
                                                          'write_answer'),
                                                   extra=0)
            
            formset_messages = MessageFormSet()


            return render(request, 
                         "logic/create_logic.html",
                         {"messages": all_messages,
                          "formset_messages": formset_messages})

    def post(self, request):
        if request.user.is_authenticated:
            MessageFormSet = modelformset_factory(Message, fields=('text_message', 
                                                                   'id_parent', 
                                                                    'display_condition',
                                                                    'write_answer'))
            
            formset_messages = MessageFormSet(request.POST)

            if formset_messages.is_valid():
                for form in formset_messages:
                    print(form.cleaned_data)
            else:
                print("Не валидные данные")
                
            return HttpResponse("ТЕСТ")

