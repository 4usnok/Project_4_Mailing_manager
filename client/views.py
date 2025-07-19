from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView

from client.forms import ClientForm
from client.models import Recipient


class MainClientView(ListView):
    """ Просмотр страницы с сообщениями """
    model = Recipient
    template_name = "client/client_list_page.html"
    context_object_name = 'client_context'

class ClientAddView(CreateView):
    """ Добавление сообщений """
    model = Recipient
    fields = '__all__'
    template_name = "client/crud/form_client.html"
    success_url = reverse_lazy('client:client_list')

class ClientFormView(FormView):
    """ Форма для клиента"""
    form_class = ClientForm
    template_name = 'client/crud/form_client.html'
    success_url = reverse_lazy('client:client_list')

    def form_valid(self, form):
        form = form.save(commit=False).save()
        return super().form_valid(form)
