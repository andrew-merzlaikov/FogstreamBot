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
    просмотреть логику
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


class ViewLogicEdit(TemplateView):

    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ViewLogicEdit, self).dispatch(*args, **kwargs)

    def get(self, request):
        """
        Возвращает форму для редактирования логики
        """
        if request.user.is_authenticated:
            
            all_messages = Message.objects.all()

            MessageFormSet = modelformset_factory(Message, 
                                                  fields=('text_message', 
                                                          'id_parent', 
                                                          'display_condition',
                                                          'write_answer'),
                                                  extra=0,
                                                  widgets={
                                                    'text_message': forms.Textarea(attrs={'cols': 80, 
                                                                                          'rows': 2}),
                                                    "write_answer": forms.CheckboxInput
                                                  })
            
            formset_messages = MessageFormSet()

            return render(request, 
                         "logic/edit_logic.html",
                         {"messages": all_messages,
                          "formset_messages": formset_messages})
        else:
            return render(request, "http_response/error_401.html", status=401)

    def put(self, request):
        """
        Редактирует логику общения
        """
        if request.user.is_authenticated:
            MessageFormSet = modelformset_factory(Message, 
                                                  fields=('text_message', 
                                                          'id_parent', 
                                                          'display_condition',
                                                          'write_answer'),
                                                  widgets={
                                                    'text_message': forms.Textarea(attrs={'cols': 80, 
                                                                                          'rows': 2}),
                                                    "write_answer": forms.CheckboxInput
                                                  }
                                                  )
            
            formset_messages = MessageFormSet(request.POST)

            if formset_messages.is_valid():
                
                if not Message.check_parent_in_messages(formset_messages):
                    url_for_redirect = reverse("appadmin:edit_logic")
                    params = "?root_errors=True"
                    url_for_redirect = url_for_redirect + params

                    return HttpResponseRedirect(url_for_redirect)


                for form in formset_messages:
                    id_msg = form.cleaned_data['id'].id                        
                    message = Message.objects.get(pk=id_msg)

                    if not Message.check_message_id_parent(form.\
                                                           cleaned_data['id_parent']):
                            
                        url_for_redirect = reverse("appadmin:edit_logic")
                        
                        params = ("?conflict_has_parent=True&id=" +
                                  str(form.cleaned_data['id_parent']))
                            
                        url_for_redirect = url_for_redirect + params

                        return HttpResponseRedirect(url_for_redirect)

                    check_parent_myself = Message.check_parent_myself(form.cleaned_data)
                        
                    if check_parent_myself is not True:
                        url_for_redirect = reverse("appadmin:edit_logic")
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

                url_for_redirect = reverse("appadmin:edit_logic")
                params = "?create_logic=True"
                url_for_redirect += params

                return HttpResponseRedirect(url_for_redirect)

            else:    
                url_for_redirect = reverse("appadmin:edit_logic")   
                str_errors = ''

                for error in formset_messages.errors:
                    str_errors += str(error)

                params = "?form_error=True&formset_errors=" + str_errors
                url_for_redirect = url_for_redirect + params

                return HttpResponseRedirect(url_for_redirect)
        else:
            return render(request, "http_response/error_401.html", status=401)

    def delete(self, request):
        """
        Удаляет логику общения
        """
        if request.user.is_authenticated:
            all_messages = Message.objects.all()

            for message in all_messages:
                message.delete()

            url_for_redirect = reverse("appadmin:edit_logic")
            params_delete = "?delete_logic=True"

            url_for_redirect = url_for_redirect + params_delete

            return HttpResponseRedirect(url_for_redirect)
        else:
            return render(request, "http_response/error_401.html", status=401)