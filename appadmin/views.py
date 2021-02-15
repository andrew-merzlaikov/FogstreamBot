from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from .models import (Sequence_Logic, 
                    Message, 
                    Question)
from .forms import (MessageForm, 
                    QuestionForm,
                    FollowForm)
from appserver.models import UserTelegram


def show_logic(request):
    if request.user.is_authenticated:
        message_questions =  Sequence_Logic.objects.all()
        list_msg_question = list()

        for msg_qu in message_questions:
            if msg_qu.message_id is not None:
                msg = Message.objects.get(pk=msg_qu.message_id)
                list_msg_question.append(msg)
            else:
                que = Question.objects.get(pk=msg_qu.question_id)
                list_msg_question.append(que)
        
        exists_logic =  Sequence_Logic.objects.all().exists()

        return render(request, 
                      "logic/show_logic.html",
                      {'list_msg_questions': list_msg_question,
                      'exists_logic': exists_logic})

class ViewMain(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            exists_data = Sequence_Logic.objects.all().exists()
            return render(request, 
                         "main.html", 
                          context={'exists_data': exists_data})
        else:
            return render(request, "http_response/error_401.html", status=401)


class ViewMessage(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            message_form = MessageForm()

            all_messages = Message.objects.all()

            return render(request, 
                         "messages/create_message.html",
                         {"form": message_form,
                          "messages": all_messages})
        else:
            return render(request, "http_response/error_401.html", status=401)

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
                return render(request, "http_response/error_401.html", status=401)
        else:
            message_form = MessageForm()

            return render(request, 
                         "messages/create_message.html",
                         {"form": message_form})


class ViewQuestion(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            question_form = QuestionForm()

            all_questions = Question.objects.all()


            return render(request, 
                         "questions/create_question.html",
                         {"form": question_form,
                          "questions": all_questions})
        else:
            return render(request, "http_response/error_401.html", status=401)
    
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
            
            all_questions = Question.objects.all()
            all_messages = Message.objects.all()
            follow_form = FollowForm()

            exists_logic =  Sequence_Logic.objects.all().exists()

            return render(request,
                          "logic/create_logic.html", 
                          {"questions": all_questions,
                           "messages": all_messages,
                           "follow_form": follow_form,
                           "exists_logic": exists_logic})
        else:
            return render(request, "http_response/error_401.html", status=401)
    
    def post(self, request):
        if request.user.is_authenticated:
            msg_question =  Sequence_Logic()
            logic_squence = msg_question.set_logic_dict(request.POST.items())

            for entities_info in logic_squence: 
                if entities_info["type"] == "message":
                    message = Message.objects.get(pk=int(entities_info["id"]))  
                    Sequence_Logic.objects.create(message=message)
                elif entities_info["type"] == "question":
                    question = Question.objects.get(pk=int(entities_info["id"]))  
                    Sequence_Logic.objects.create(question=question)

            return redirect('bot/logic')
        else:
            return render(request, "http_response/error_401.html", status=401)