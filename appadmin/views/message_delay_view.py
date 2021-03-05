from django.views.generic.base import TemplateView
from appadmin.models import (Message,
                             MessageDelay)
from appadmin.forms import (MessageForm,
                            MessageDelayForm)
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect


def show_edit_delay(request, id_message):
    """
    Возвращает форму для редактирования задержки
    сообщения
    """

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


class ViewMessageDelay(TemplateView):

    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ViewMessageDelay, self).dispatch(*args, **kwargs)

    def get(self, request):
        """
        Возвращает таблицу с которой можно выбрать 
        нужное сообщения для задания задержки
        """
        if request.user.is_authenticated:
            messages_all = Message.objects.all()
            messages_with_delay = MessageDelay.\
                                    objects.\
                                    all()


            return render(request, 
                        "delay/delays.html", 
                        {"messages_all": messages_all,
                        "messages_delay": messages_with_delay})
        else:
            return render(request, "http_response/error_401.html", status=401)
    
    def post(self, request, id_message):
        """
        Устанавливает задержку для сообщения
        """
        if request.user.is_authenticated:
            delay = request.POST['delay']

            person, created = MessageDelay.objects.update_or_create(
                    message_id=id_message, defaults={"delay": delay}
            )
            
            params = "?set_delay=True"
            url_for_redirect = reverse('appadmin:delay_get') + params

            return HttpResponseRedirect(url_for_redirect)
        else:
            return render(request, "http_response/error_401.html", status=401)
    
    def delete(self, request, id_message):
        """
        Позволяет удалить задержку
        """
        if request.user.is_authenticated:


            message_exists = MessageDelay.\
                             objects.\
                             filter(message_id=id_message).\
                             exists()

            if message_exists:
                MessageDelay.\
                objects.\
                filter(message_id=id_message).\
                delete()
            
            params = "?delete_delay=True"
            url_for_redirect = reverse('appadmin:delay_get') + params

            return HttpResponseRedirect(url_for_redirect)
        else:
            return render(request, "http_response/error_401.html", status=401)