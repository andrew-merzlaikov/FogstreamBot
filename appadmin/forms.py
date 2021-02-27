from django import forms
from .models import Message

class MessageForm(forms.Form):
    text_message = forms.CharField(max_length=100,
                                   widget=forms.Textarea(attrs={
                                                            'rows': 2, 
                                                            'cols': 60}))
    


