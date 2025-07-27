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
        """ Отображение рассылок """
        context = super().get_context_data(**kwargs)

        # Пропишем переменные для обращения к моделям рассылок
        active_count = Newsletter.objects.filter(status="Запущена").count()
        total_count = Newsletter.objects.count()
        unique_clients = Recipient.objects.distinct().count()

        context.update(
            {
                'item_count': total_count, # количество всех рассылок
                'active_count': active_count, # количество активных рассылок
                'unique_clients': unique_clients, # количество уникальных получателей
            }
        )
        return context

