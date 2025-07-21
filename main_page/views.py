from django.shortcuts import render
from django.views.generic import ListView
from client.models import Recipient

from mailings.models import Newsletter
from main_page.models import Home


class MainView(ListView):
    """ Просмотр главной страницы """
    model = Home
    template_name = "main_page/home_page.html"
    context_object_name = 'main_context'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'item_count': Newsletter.objects.count(),
                'active_count': Newsletter.objects.filter(status="Запущена").count(),
                'unique_clients': Recipient.objects.distinct().count(),
            }
        )
        return context
