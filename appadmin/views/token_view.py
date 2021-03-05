from django.views.generic.base import TemplateView
from appadmin.models import TokenBot
from appadmin.forms import TokenBotForm
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect


class ViewToken(TemplateView):
    def get(self, request):
        """
        Возвращает страницу через которую можно поставить
        токен
        """
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
        """
        Позволяет установить значения токена
        """
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
        else:
            return render(request, "http_response/error_401.html", status=401)