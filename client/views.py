from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, DeleteView, UpdateView, DetailView

from client.forms import ClientForm
from client.models import Recipient


class MainClientView(ListView):
    """ Просмотр страницы с клиентами """
    model = Recipient
    template_name = "client/client_list_page.html"
    context_object_name = 'client_context'

class ClientAddView(CreateView):
    """ Добавление клиентов """
    model = Recipient
    fields = '__all__'
    template_name = "client/crud/form_client.html"
    success_url = reverse_lazy('client:client_list')

class ClientDeleteView(DeleteView):
    """ Удаление клиентов """
    model = Recipient
    fields = '__all__'
    template_name = "client/crud/client_delete.html"
    success_url = reverse_lazy('client:client_list')

class ClientUpdateView(UpdateView):
    """ Редактирование клиентов """
    model = Recipient
    fields = '__all__'
    template_name = "client/crud/form_client.html"
    success_url = reverse_lazy('client:client_list')

class ClientDetailView(DetailView):
    """ Подробная информация клиентов """
    model = Recipient
    fields = '__all__'
    template_name = "client/crud/client_detail.html"
    success_url = reverse_lazy('client:forms_detail')

class ClientFormView(FormView):
    """ Форма для клиента"""
    form_class = ClientForm
    template_name = 'client/crud/form_client.html'
    success_url = reverse_lazy('client:client_list')

    def form_valid(self, form):
        form = form.save(commit=False).save()
        return super().form_valid(form)
