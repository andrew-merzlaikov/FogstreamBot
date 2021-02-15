from django import forms


class MessageForm(forms.Form):
    text_message = forms.CharField(max_length=150,
                                   widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 60}))
    

class QuestionForm(forms.Form):
    question = forms.CharField(max_length=150, 
                               label="Введите вопрос",
                               widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 60}))

    question_confirm = forms.CharField(max_length=50,
                                      label="Что увидит пользователь "
                                            "если утвердительно ответит на вопрос",
                                      required=False,
                                      widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 60}))

    question_not_confirm = forms.CharField(max_length=50,
                                           label="Что увидит пользователь "
                                                 "если отрицательно ответит на вопрос",
                                           required=False,
                                           widget=forms.Textarea(attrs={
                                                                'rows': 2, 
                                                                'cols': 60}))