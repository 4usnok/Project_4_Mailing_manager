from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        labels = {
            'topic_mail': 'Тема письма',
            'body_mail': 'Тело письма',
        }
