from datetime import timedelta, datetime

from django.db import models
from django.db.models.functions import Now, TruncMonth

from client.models import Recipient
from message.models import Message


class Newsletter(models.Model):
    """ Модель 'Сообщение' """
    CREATED = 'Создана'
    LAUNCHED = 'Запущена'
    COMPLETED = 'Завершена'
    STATUS_MAILING = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    dt_of_first_shipment = models.DateTimeField(auto_now_add=True)
    end_dt_of_sending = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_MAILING, default=CREATED, verbose_name="статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)

    class Meta:
        ordering = [
            'dt_of_first_shipment',
            'end_dt_of_sending',
            'status',
            'message',
        ]

    def __str__(self):
        return self.status

class MailingAttempt(models.Model):
    """ Модель 'Попытка рассылки' """
    SUCCESSFUL = 'Успешно'
    NOT_SUCCESSFUL = 'Не успешно'
    STATUS_OF_ATTEMPT = [
        (SUCCESSFUL, 'Успешно'),
        (NOT_SUCCESSFUL, 'Не успешно'),
    ]

    dt_of_attempt = models.DateTimeField(default=datetime.now)
    status_of_attempt = models.CharField(max_length=100, choices=STATUS_OF_ATTEMPT, default=SUCCESSFUL, verbose_name="Статус попытки рассылки")
    answer_server = models.TextField(null=True, blank=True, max_length=20,)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)

    class Meta:
        ordering = [
            'dt_of_attempt',
            'status_of_attempt',
            'answer_server',
            'newsletter',
        ]

        def __str__(self):
            return self.answer_server
