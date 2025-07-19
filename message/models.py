from django.db import models

class Message(models.Model):
    """ Модель 'Сообщение' """
    topic_mail = models.CharField()
    body_mail = models.TextField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = [
            'topic_mail',
            'body_mail',
        ]

    def __str__(self):
        return self.topic_mail