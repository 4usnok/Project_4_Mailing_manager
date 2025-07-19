from django.views.generic import ListView

from main_page.models import Home


class MainView(ListView):
    """ Просмотр главной страницы """
    model = Home
    template_name = "main_page/home_page.html"
    context_object_name = 'main_context'
