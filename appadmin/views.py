from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from .models import (Message_Question, 
                    Message, 
                    Question)
from .forms import MessageForm, QuestionForm
from appserver.models import UserTelegram


class ViewMain(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            exists_data = Message_Question.objects.all().exists()
            return render(request, 
                         "main.html", 
                          context={'exists_data': exists_data})
        else:
            return HttpResponse("You not auth bro")


class ViewMessage(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            message_form = MessageForm()

            all_messages = Message.objects.all()

            return render(request, 
                         "create_message.html",
                         {"form": message_form,
                          "messages": all_messages})
        else:
            return HttpResponse("You not auth bro")
    
    def post(self, request):
        if request.method == "POST" and request.user.is_authenticated:
            message_form = MessageForm(request.POST)
            
            if message_form.is_valid():
                context_data = {
                    "message": message_form.cleaned_data["text_message"]
                }

                Message.objects.create(text_message=context_data['message'])

                return redirect('/bot/message?' + 'status_msg=OK')
            else:
                return HttpResponse("Invalid Data")
        else:
            message_form = MessageForm()

            return render(request, 
                         "create_message.html",
                         {"form": message_form})


class ViewQuestion(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            question_form = QuestionForm()

            all_questions = Question.objects.all()


            return render(request, 
                         "create_question.html",
                         {"form": question_form,
                          "questions": all_questions})
        else:
            return render("You not auth bro")
    
    def post(self, request):
        if request.user.is_authenticated:
            question_form = QuestionForm(request.POST)
            
            if question_form.is_valid():
                context_data = {
                    "question": question_form.cleaned_data["question"],
                    "question_confirm": question_form.\
                                        cleaned_data["question_confirm"],
                    "question_not_confirm": question_form.\
                                            cleaned_data["question_not_confirm"],
                }

                Question.objects.create(question=context_data['question'],
                                        question_confirm=context_data['question_confirm'],
                                        question_not_confirm=context_data['question_not_confirm'])

                return redirect('/bot/question?' + 'status_question=OK')
            else:
                return HttpResponse("Invalid Data")
        else:
            question_form = QuestionForm()

            return render(request, 
                         "create_message.html",
                         {"form": question_form})
        


class ViewUser(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            users_telegrams = UserTelegram.objects.all()

            return render(request, 
                         "users.html",
                         {"users_telegram": users_telegrams})
        else:
            return HttpResponse("Not auth bro")


class ViewLogic(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request,
                          "logic.html")
        else:
            return HttpResponse("Not auth bro")