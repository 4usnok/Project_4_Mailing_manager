from django.shortcuts import render
from django.views.generic import ListView
from client.models import Recipient

from mailings.models import Newsletter
from message.models import Message
from users.forms import UserRegistrationForm
from main_page.models import Home


class MainView(ListView):
    """ Просмотр главной страницы """
    model = Home
    template_name = "main_page/home_page.html"
    context_object_name = 'main_context'

    def get_context_data(self, **kwargs):
        """ Отображение рассылок """
        context = super().get_context_data(**kwargs)
        # Пропишем переменные для обращения к модели рассылок
        completed_count = Newsletter.objects.filter(status="Завершена").count()
        active_count = Newsletter.objects.filter(status="Запущена").count()
        total_count = Newsletter.objects.count()
        unsuccessful_mailings = Newsletter.objects.exclude(status="Завершена").count()

        context.update(
            {
                'item_count': total_count, # количество всех рассылок
                'active_count': active_count, # количество активных рассылок
                'unique_clients': Recipient.objects.distinct().count(), # количество уникальных получателей
                'successful_mailings': completed_count,  # успешные попытки рассылок
                'unsuccessful_mailings': unsuccessful_mailings,  # неуспешные попытки рассылок
                'sent_messages': completed_count,  # количество отправленных сообщений
            }
        )
        return context

