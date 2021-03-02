from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect
from .models import (Message, 
                     TokenBot,
                     MessageDelay)
from .forms import (MessageForm,
                    TokenBotForm,
                    MessageDelayForm)
from django.urls import reverse
from appserver.models import UserTelegram
import operator


def show_edit_delay(request, id_message):
    if request.user.is_authenticated:
        message = Message.\
                  objects.\
                  filter(id=id_message).get()
        
        message_delay_form = MessageDelayForm()

        return render(request, 
                      "delay/show_edit_delay.html",
                      {"message": message,
                       "message_delay_form": message_delay_form})
    else:
        return render(request, "http_response/error_401.html", status=401)

def show_edit_form_message(request, id_message):
    if request.user.is_authenticated:
        message_form = MessageForm()
        return render(request, 
                      "messages/edit_message.html", 
                      {'message_form': message_form,
                       'id_message': id_message})
    else:
        return render(request, "http_response/error_401.html", status=401)


class ViewMessageDelay(TemplateView):
    def get(self, request):

        messages_all = Message.objects.all()
        messages_with_delay = MessageDelay.\
                                  objects.\
                                  all()


        return render(request, 
                      "delay/delays.html", 
                      {"messages_all": messages_all,
                       "messages_delay": messages_with_delay})
    
    def post(self, request, id_message):
        
        delay = request.POST['delay']

        person, created = MessageDelay.objects.update_or_create(
                message_id=id_message, defaults={"delay": delay}
        )

        return HttpResponseRedirect(reverse('appadmin:delay_get'))
    

class ViewToken(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            token_bot_form = TokenBotForm()
            token = TokenBot.objects.first()

            return render(request,
                        "token/token.html",
                        {"token_form": token_bot_form,
                         "token": token})
        else:
            return render(request, "http_response/error_401.html", status=401)

    def post(self, request):
        if request.user.is_authenticated:
            exists_token = TokenBot.\
                           objects.\
                           first()
            
            if exists_token:
                TokenBot.objects.first().delete()
                TokenBot.objects.create(token_bot=request.POST['token_bot'])
            else:
                TokenBot.objects.create(token_bot=request.POST['token_bot'])

            url_for_redirect = reverse('appadmin:token_get')

            return HttpResponseRedirect(url_for_redirect)

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
            
            all_messages = Message.\
                           objects.\
                           all()

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

    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ViewLogic, self).dispatch(*args, **kwargs)

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
            MessageFormSet = modelformset_factory(Message, 
                                                  fields=('text_message', 
                                                          'id_parent', 
                                                          'display_condition',
                                                          'write_answer'),
                                                    )
            
            formset_messages = MessageFormSet(request.POST)

            if formset_messages.is_valid():
                

                if not Message.check_parent_in_messages(formset_messages):
                    url_for_redirect = reverse("appadmin:create_logic")
                    params = "?root_errors=True"
                    url_for_redirect = url_for_redirect + params

                    return HttpResponseRedirect(url_for_redirect)


                for form in formset_messages:
                    id_msg = form.cleaned_data['id'].id                        
                    message = Message.objects.get(pk=id_msg)

                    if not Message.check_message_id_parent(form.\
                                                           cleaned_data['id_parent']):
                            
                        url_for_redirect = reverse("appadmin:create_logic")
                        params = ("?conflict_has_parent=True&id=" +
                                      str(form.cleaned_data['id_parent']))
                            
                        url_for_redirect = url_for_redirect + params

                        return HttpResponseRedirect(url_for_redirect)

                    check_parent_myself = Message.check_parent_myself(form.cleaned_data)
                        
                    if check_parent_myself is not True:
                        url_for_redirect = reverse("appadmin:create_logic")
                        params = ("?error_parent_myself=" + check_parent_myself["message"])
                        url_for_redirect = url_for_redirect + params

                        return HttpResponseRedirect(url_for_redirect)


                    message.id_parent = form.\
                                        cleaned_data['id_parent']

                    message.\
                    display_condition = form.\
                                        cleaned_data['display_condition']
                        
                    message.\
                    write_answer = form.cleaned_data['write_answer']

                    message.save()

                url_for_redirect = reverse("appadmin:create_logic")
                params = "?create_logic=True"
                url_for_redirect += params

                return HttpResponseRedirect(url_for_redirect)

            else:    
                url_for_redirect = reverse("appadmin:create_logic")   
                str_errors = ''

                for error in formset_messages.errors:
                    str_errors += str(error)

                params = "?form_error=True&formset_errors=" + str_errors
                url_for_redirect = url_for_redirect + params

                return HttpResponseRedirect(url_for_redirect)

    def delete(self, request):

        all_messages = Message.objects.all()

        for message in all_messages:
            message.id_parent = None
            message.display_condition = None
            message.write_answer = None
            message.save()

        url_for_redirect = reverse("appadmin:create_logic")
        params_delete = "?delete_logic=True"

        url_for_redirect = url_for_redirect + params_delete

        return HttpResponseRedirect(url_for_redirect)