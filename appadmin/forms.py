from django import forms


class MessageForm(forms.Form):
    text_message = forms.CharField(max_length=150)


class Question(forms.Form):
    question = forms.CharField(max_length=150)
    confirm = forms.CharField(max_length=50)

    question_confirm = forms.CharField(max_length=50)
    question_not_confirm = forms.CharField(max_length=50)