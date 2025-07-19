from django.db import models

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
