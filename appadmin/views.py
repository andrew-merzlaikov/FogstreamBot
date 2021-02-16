from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.template.response import TemplateResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect
from .models import (Sequence_Logic, 
                    Message, 
                    Question)
from .forms import (MessageForm, 
                    QuestionForm)
from django.urls import reverse
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

                return redirect('/bot/create/message')
        else:
            return render(request, "http_response/error_401.html", status=401)

    def delete(self, request, id_message):
        if request.user.is_authenticated:
            
            Message.objects.\
                            filter(id=id_message).delete()
            
            Sequence_Logic.objects.\
                          filter(message_id=id_message).delete()

            return  redirect('/bot/create/message')
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

                Question.objects.create(question=context_data['question'],
                                        question_confirm=context_data['question_confirm'],
                                        question_not_confirm=context_data['question_not_confirm'])

                return redirect('/bot/create/question?' + 'status_question=OK')
            else:
                return HttpResponse("Invalid Data")
        else:
            return render(request, "http_response/error_401.html", status=401)
    
    def put(self, request, id_question):
        if request.user.is_authenticated:
            form = QuestionForm(request.POST or None)
            
            if form.is_valid():
                question_text = form.cleaned_data.get("question")
                text_confirm = form.cleaned_data.get("question_confirm")
                text_not_confirm = form.cleaned_data.get("question_not_confirm")
                
                Question.\
                        objects.\
                        filter(id=id_question).\
                        update(question=question_text,
                               question_confirm=text_confirm,
                               question_not_confirm=text_not_confirm)

                return redirect('/bot/create/question')
        else:
            return render(request, "http_response/error_401.html", status=401)

    def delete(self, request, id_question):
        if request.user.is_authenticated:
            
            Question.objects.\
                            filter(id=id_question).delete()
            
            Sequence_Logic.objects.\
                          filter(question_id=id_question).delete()

            return  redirect('/bot/create/question')
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
            message_form_set = modelformset_factory(Message,
                                                    fields=('text_message',),
                                                    can_order=True,
                                                    extra=0)

            question_form_set = modelformset_factory(Question,
                                                    fields=('question',),
                                                    can_order=True,
                                                    extra=0)
            
            some_formset = question_form_set(initial=[{'id': x.id} 
                                                                for x in all_messages])

            return render(request,
                          "logic/create_logic.html", 
                          {"questions": all_questions,
                           "messages": all_messages,
                           "message_set": message_form_set,
                           "questions_set": question_form_set,
                           "exists_logic": exists_logic})
        else:
            return render(request, "http_response/error_401.html", status=401)
    
    def post(self, request):
        if request.user.is_authenticated:
            msg_question =  Sequence_Logic()
            # data_list_post = list(request.POST)
            # data = data_list_post[5:len(data_list_post)]
            
            message_form_set = modelformset_factory(Message,
                                                    fields=('text_message',),
                                                    can_order=True,
                                                    extra=0)

            question_form_set = modelformset_factory(Question,
                                                    fields=('question',),
                                                    can_order=True,
                                                    extra=0)

            questionForm = question_form_set(request.POST)
            messageForm = message_form_set(request.POST)

            for question in questionForm:
                print(question)
            
            for message in messageForm:
                print(message.cleaned_data)

            # logic_squence = msg_question.set_logic_dict(request.POST,
            #                                             message_form_set,
            #                                             question_form_set)


            # for entities_info in logic_squence: 
            #     print(entities_info)
                # if entities_info["type"] == "message":
                #     message = Message.objects.get(pk=entities_info["id"])  
                #     # Sequence_Logic.objects.create(message=message)
                # elif entities_info["type"] == "question":
                #     question = Question.objects.get(pk=entities_info["id"])  
                #     # Sequence_Logic.objects.create(question=question)

            return HttpResponse(request.POST)
        else:
            return render(request, "http_response/error_401.html", status=401)
        
    def delete(self, request):
        if request.user.is_authenticated:
            Sequence_Logic.objects.all().delete()
            
            return HttpResponseRedirect(reverse("appadmin:create_logic"))
        else:
            return render(request, "http_response/error_401.html", status=401)