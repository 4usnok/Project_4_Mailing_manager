from django.db import models


class UsersModels(models.Model):
    """ Модель 'Пользователи' """

    email_name = models.CharField(unique=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = [
            'email_name',
        ]

    def __str__(self):
        return self.email_name