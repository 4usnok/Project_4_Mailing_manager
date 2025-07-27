from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    """ Модель 'Сообщение' """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_mail = models.CharField()
    body_mail = models.TextField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = [
            'topic_mail',
            'body_mail',
        ]

    def __str__(self):
        return self.topic_mail