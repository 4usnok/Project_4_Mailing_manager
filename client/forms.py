from django import forms
from .models import Recipient


class ClientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'
        labels = {
            'email': 'почта',
            'full_name': 'ФИО',
            'comment': 'комментарий',
        }
