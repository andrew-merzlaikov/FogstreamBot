from django import forms
from .models import Message

class MessageForm(forms.Form):
    text_message = forms.CharField(max_length=500,
                                   widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 60}))
    
class MessageLogicForm(forms.Form):
    text_message = forms.CharField(max_length=100,
                                   widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 60}))
    
    write_answer = forms.CheckboxInput()

class TokenBotForm(forms.Form):
    token_bot = forms.CharField(max_length=500,
                                widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 120}))


class MessageDelayForm(forms.Form):
    delay = forms.IntegerField()
    
