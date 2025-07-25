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
        unsuccessful_mailings = 0
        if Newsletter.objects.filter(status="Запущена").count():
            unsuccessful_mailings += 1
        context.update(
            {
                'item_count': Newsletter.objects.count(), # количество всех рассылок
                'active_count': Newsletter.objects.filter(status="Запущена").count(), # количество активных рассылок
                'unique_clients': Recipient.objects.distinct().count(), # количество уникальных получателей
                'successful_mailings': Newsletter.objects.filter(status="Запущена").count(),  # успешные попытки рассылок
                'unsuccessful_mailings': Newsletter.objects.filter(status="Создана").count(),  # неуспешные попытки рассылок
                'sent_messages': unsuccessful_mailings,  # количество отправленных сообщений
            }
        )
        return context

