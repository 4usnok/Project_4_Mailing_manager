from django import forms

from mailings.models import Newsletter


class MailingsForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'
        labels = {
            'dt_of_first_shipment': 'Дата и время первой отправки',
            'end_dt_of_sending': 'Дата и время окончания отправки',
            'status': 'Статус',
            'message': 'Сообщение',
            'recipients': 'Получатели',
        }