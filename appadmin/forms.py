from django import forms
from .models import Message


class MessageForm(forms.Form):
    """
    Форма для задания сообщений
    text_message - текст сообщения
    write_answer - является ли сообщение вопросом
    display_condition - условие отображения если это вопрос
    """
    text_message = forms.CharField(max_length=500,
                                   widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 60}),
                                   label="Текст сообщения")

    write_answer = forms.BooleanField(label="Сообщение является вопросом?",
                                      required=False) 

    display_condition = forms.CharField(max_length=100,
                                        widget=forms.Textarea(attrs={
                                                            'rows': 1, 
                                                            'cols': 60}),
                                        label="Как надо ответить" 
                                              "на родительский "
                                              "вопрос, чтобы это сообщение" 
                                              "было показано?",
                                        required=False,
                                        initial=None)


class CountChildsMessageForm(forms.Form):
    """
    Форма которая позволяет задать количество детей
    у данного сообщения
    count_childs - количество потомков
    """

    count_childs = forms.IntegerField(min_value=1,
                                      label="Задайте количество потомков")


class TokenBotForm(forms.Form):
    """
    Форма для задания токена бота
    token_bot - текст с токеном
    """
    token_bot = forms.CharField(max_length=500,
                                widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 120}))


class MessageDelayForm(forms.Form):
    """
    Форма для задания задержки
    delay - задержка появления сообщения
    """
    delay = forms.IntegerField(min_value=1)
    
