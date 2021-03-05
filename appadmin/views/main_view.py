from django.views.generic.base import TemplateView
from django.shortcuts import render


class ViewMain(TemplateView):
    def get(self, request):
        """
        Возвращает главную страницу в панели администратора
        """
        if request.user.is_authenticated:
            return render(request, 
                         "main.html")
        else:
            return render(request, "http_response/error_401.html", status=401)
