from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect
from .models import (Sequence_Logic, 
                    User_Sequence_Logic,
                    Message, 
                    Question)
from .forms import (MessageForm, 
                    QuestionForm)
from django.urls import reverse
from appserver.models import UserTelegram
import operator


def set_logic(request):
    if request.user.is_authenticated:

        messages = Message.objects.all()
        questions = Question.objects.all()

        logic_list = list()

        for message in messages:
            logic_dict = dict()
            logic_dict["type"] = "message"
            logic_dict["id"] = message.id
            
            if message.logic_order is not None:
                logic_dict["order"] = message.logic_order
            
            logic_list.append(logic_dict)

        for question in questions:

            logic_dict = dict()
            logic_dict["type"] = "question"
            logic_dict["id"] = question.id

            if question.logic_order is not None:
                logic_dict["order"] = question.logic_order
            
            logic_list.append(logic_dict)

        logic_list.sort(key=operator.itemgetter('order'))        

        for logic_dict in logic_list:
            if logic_dict["type"] == "message":
                Sequence_Logic.objects.create(message_id=logic_dict["id"])
            elif logic_dict["type"] == "question":
                Sequence_Logic.objects.create(question_id=logic_dict['id'])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "http_response/error_401.html", status=401)

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
    else:
        return render(request, "http_response/error_401.html", status=401)

def show_edit_form_question(request, id_question):
    if request.user.is_authenticated:
        question_form = QuestionForm()
        return render(request, 
                      "questions/edit_question.html", 
                      {'question_form': question_form,
                       'id_question': id_question})

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
            exists_data = Sequence_Logic.objects.all().exists()
            return render(request, 
                         "main.html", 
                          context={'exists_data': exists_data})
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
            
            Sequence_Logic.\
                          objects.\
                          filter(message_id=id_message).\
                          delete()

            User_Sequence_Logic.\
                                objects.\
                                all().\
                                delete()

            return redirect('/bot/create/message?msg_delete=OK')
        else:
            return render(request, "http_response/error_401.html", status=401)


class ViewQuestion(TemplateView):

    http_method_names = ['get', 'post', 'put', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ViewQuestion, self).dispatch(*args, **kwargs)

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

                Question.\
                objects.\
                create(question=context_data['question'],
                       question_confirm=context_data['question_confirm'],
                       question_not_confirm=context_data['question_not_confirm'])

                return redirect('/bot/create/question?' + 'status_question=OK')
            else:
                return render(request, 
                              "http_response/error_422.html", 
                              status=422)
        else:
            return render(request, 
                          "http_response/error_401.html", 
                          status=401)
    
    def put(self, request, id_question):
        if request.user.is_authenticated:
            
            form = QuestionForm(request.POST or None)
            
            if form.is_valid():
                question_text = form.\
                                cleaned_data.\
                                get("question")
                
                text_confirm = form.\
                               cleaned_data.\
                               get("question_confirm")
                
                text_not_confirm = form.\
                                   cleaned_data.\
                                   get("question_not_confirm")
                
                Question.\
                        objects.\
                        filter(id=id_question).\
                        update(question=question_text,
                               question_confirm=text_confirm,
                               question_not_confirm=text_not_confirm)

                return redirect('/bot/create/question?que_edit=OK')
            else:
                return render(request, 
                              "http_response/error_422.html", 
                              status=422)

        else:
            return render(request, "http_response/error_401.html", status=401)

    def delete(self, request, id_question):
        if request.user.is_authenticated:
            
            Question.objects.\
                            filter(id=id_question).delete()
            
            Sequence_Logic.objects.\
                          filter(question_id=id_question).delete()

            return  redirect('/bot/create/question?que_delete=OK')
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
            
            all_questions = Question.objects.all()
            all_messages = Message.objects.all()

            exists_logic =  Sequence_Logic.objects.all().exists()
            
            messageFormSet = modelformset_factory(Message, 
                                                  fields=('text_message',),
                                                  can_order=True,
                                                  extra=0)
            

            questionFormSet = modelformset_factory(Question,
                                                    fields=('question',),
                                                    can_order=True,
                                                    extra=0,
                                                    labels = {
                                                        "Order": "Порядок в логике",
                                                    })
            
            return render(request,
                          "logic/create_logic.html", 
                          {"questions": all_questions,
                           "messages": all_messages,
                           "messages_set": messageFormSet,
                           "questions_set": questionFormSet,
                           "exists_logic": exists_logic})
        else:
            return render(request, "http_response/error_401.html", status=401)
    
    def post(self, request):
        if request.user.is_authenticated:

            messageFormSet = modelformset_factory(Message, 
                                                  fields=('text_message',),
                                                  can_order=True,
                                                extra=0)
                
            message_formset = messageFormSet(request.POST)
           
            questionFormSet = modelformset_factory(Question, 
                                                    fields=('question', ),
                                                    can_order=True,
                                                    extra=0)

            question_formset = questionFormSet(request.POST)

            if message_formset.is_valid():
        
                for form in message_formset:                    
                    msg = form.cleaned_data['id']
                    order = form.cleaned_data['ORDER']
                    
                    msg = Message.objects.\
                                         filter(id=msg.id).\
                                         update(logic_order=order)

                messages.add_message(request, 
                                     messages.INFO, 
                                     'В логике порядок для сообщений задан')
                

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif question_formset.is_valid():

                for form in question_formset:
                    que = form.cleaned_data['id']
                    order = form.cleaned_data['ORDER']

                    que = Question.objects.\
                                         filter(id=que.id).\
                                         update(logic_order=order)

                
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, "http_response/error_401.html", status=401)
        
    def delete(self, request):
        if request.user.is_authenticated:
            Sequence_Logic.objects.all().delete()
            User_Sequence_Logic.objects.all().delete()

            return HttpResponseRedirect(reverse("appadmin:create_logic"))
        else:
            return render(request, "http_response/error_401.html", status=401)