from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView


class BotView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse("You auth bro")
        else:
            return HttpResponse("You not auth bro")
