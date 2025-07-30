from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from client.models import Recipient
from mailings.models import Newsletter
from main_page.models import Home


@method_decorator(cache_page(60 * 15), name="dispatch")
class MainView(ListView):
    """ Просмотр главной страницы """
    model = Home
    template_name = "main_page/home_page.html"
    context_object_name = 'main_context'

    def get_queryset(self):
        """ низкоуровневое кэширование """
        queryset = cache.get('main_context')
        if not queryset:
            queryset = super().get_queryset()
            cache.get('main_context_queryset', queryset, 60 * 15)
        return queryset

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

