from django import forms


class MessageForm(forms.Form):
    text_message = forms.CharField(max_length=150)


class QuestionForm(forms.Form):
    question = forms.CharField(max_length=150, 
                               label="Введите вопрос")
    confirm = forms.CharField(max_length=50,
                              label="Что необходимо ответить чтобы "
                                    "ответить на вопрос правильно?")

    question_confirm = forms.CharField(max_length=50,
                                      label="Что увидит пользователь "
                                            "если правильно ответит на вопрос")
    question_not_confirm = forms.CharField(max_length=50,
                                           label="Что увидит пользователь "
                                                 "если неправильно ответит на вопрос")