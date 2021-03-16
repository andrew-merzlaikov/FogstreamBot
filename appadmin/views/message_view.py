from django.views.generic.base import TemplateView
from appadmin.models import Message
from appadmin.forms import MessageForm
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect


def show_edit_form_message(request, id_message):
    """
    Возвращает форму для редактирования сообщения
    если пользователь авторизован, иначе вернет ошибку
    :param id_message: id сообщения
    :type id_message: int
    """

    if request.user.is_authenticated:

        message = Message.\
                  objects.\
                  filter(id=id_message).\
                  get()

        dict_initial_form = {
            "text_message": message.text_message,
            "write_answer": message.write_answer,
            "display_condition": message.display_condition
        }

        message_form = MessageForm(initial=dict_initial_form)

        return render(request, 
                      "messages/edit_message.html", 
                      {'message_form': message_form,
                       'id_message': id_message,
                       'message': message})
    else:
        return render(request, 
                      "http_response/error_401.html", 
                      status=401)

def set_root_message(request):
    """
    Устанавливает корневое сообщение если 
    пользователь авторизован, иначе вернет ошибку
    """
    if request.user.is_authenticated:
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            Message.\
            objects.\
            create(text_message=message_form.\
                                cleaned_data['text_message'],
                   id_parent=0,
                   write_answer=message_form.\
                                cleaned_data['write_answer'])

            url_for_redirect = reverse('appadmin:get_create_logic')

            return HttpResponseRedirect(url_for_redirect)
    else:
        return render(request, 
                      "http_response/error_401.html", 
                      status=401)


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
        """
        Возвращает таблицу через которую можно 
        редактировать и удалять сообщения если пользователь
        авторизован, иначе вернет ошибку
        """
        if request.user.is_authenticated:
            message_form = MessageForm()
            
            all_messages = Message.\
                           objects.\
                           all()

            return render(request, 
                         "messages/edit_messages.html",
                         {"form": message_form,
                          "messages": all_messages})
        else:
            return render(request, 
                          "http_response/error_401.html", 
                          status=401)

    def post(self, request):
        """
        Сохраняет созданное общение при создании логики
        если пользователь авторизован, иначе вернет ошибку
        """
        if request.user.is_authenticated:
            message_form = MessageForm(request.POST)
            
            if message_form.is_valid():
                

                context_data = {
                    "message": message_form.cleaned_data["text_message"],
                    "write_answer": message_form.cleaned_data["write_answer"],
                }

                Message.objects.create(text_message=context_data['message'],
                                       write_answer=context_data["write_answer"])

                return redirect('/bot/create/message?' + 'status_msg=OK')
            else:
                return render(request, 
                              "http_response/error_422.html", 
                              status=422)

        else:
            return render(request, 
                          "http_response/error_401.html", 
                          status=401)

    def put(self, request, id_message):
        """
        Обновляет сообщение при редактировании 
        если пользователь авторизован
        иначе вернет ошибку
        :param id_message: id сообщения
        :type id_message: int
        """
        if request.user.is_authenticated:
            form = MessageForm(request.POST or None)

            if form.is_valid():
                text_message = form.cleaned_data.get("text_message")
                write_answer = form.cleaned_data.get('write_answer')
                display_condition = None

                if form.cleaned_data.get('display_condition') != '':
                    display_condition = form.\
                                        cleaned_data.\
                                        get('display_condition')

                    display_condition = display_condition.lower()

                Message.\
                        objects.\
                        filter(id=id_message).\
                        update(text_message=text_message,
                               write_answer=write_answer,
                               display_condition=display_condition)
                

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return render(request, 
                              "http_response/error_422.html", 
                              status=422)

        else:
            return render(request, 
                          "http_response/error_401.html", 
                          status=401)

    def delete(self, request, id_message):
        """
        Удаляет сообщение из Базы данных если пользователь
        авторизован, иначе вернет ошибку
        :param id_message: id сообщения которого необходимо удалить
        :type id_message: int
        """
        if request.user.is_authenticated:
            
            Message.\
                    objects.\
                    filter(id=id_message).\
                    delete()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, 
                          "http_response/error_401.html", 
                           status=401)