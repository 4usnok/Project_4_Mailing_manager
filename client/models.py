from django.contrib.auth.models import User
from django.db import models

class Recipient(models.Model):
    """ Модель 'Получатель рассылки' """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'получатель рассылки'
        verbose_name_plural = 'получатели рассылки'
        ordering = [
            'email',
            'full_name',
            'comment',
        ]
        permissions = [
            ("can_view_for_manager", "Can view for manager"),
        ]


    def __str__(self):
        return self.email
