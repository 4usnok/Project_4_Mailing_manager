from django.db import models

class Recipient(models.Model):
    """ Модель 'Сообщение' """
    email = models.CharField(unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = [
            'email',
            'full_name',
            'comment',
        ]

    def __str__(self):
        return self.email
