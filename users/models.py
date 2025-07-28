from django.contrib.auth.models import User
from django.db import models


class UsersList(models.Model):
    """ Модель 'Пользователи' """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email_name = models.CharField(unique=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = [
            'owner',
            'email_name',
        ]
        permissions = [
            ("can_view_for_list_user", "Can view for list user"),
        ]

    def __str__(self):
        return self.owner