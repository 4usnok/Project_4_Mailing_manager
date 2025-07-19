from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView

from mailings.forms import MailingsForm
from mailings.models import Newsletter


class MainMailingsView(ListView):
    """ Просмотр страницы с сообщениями """
    model = Newsletter
    template_name = "mailings/mailings_list_page.html"
    context_object_name = 'mailings_context'

class MailingsAddView(CreateView):
    """ Добавление клиентов """
    model = Newsletter
    fields = '__all__'
    template_name = "mailings/crud/form_mailings.html"
    success_url = reverse_lazy('mailings:mailings_list')

class MailingsDeleteView(DeleteView):
    """ Удаление клиентов """
    model = Newsletter
    fields = '__all__'
    template_name = "mailings/crud/mailings_delete.html"
    success_url = reverse_lazy('mailings:mailings_list')

class MailingsUpdateView(UpdateView):
    """ Редактирование клиентов """
    model = Newsletter
    fields = '__all__'
    template_name = "mailings/crud/form_mailings.html"
    success_url = reverse_lazy('mailings:mailings_list')

class MailingsFormView(FormView):
    """ Форма для клиента"""
    form_class = MailingsForm
    template_name = 'mailings/crud/form_mailings.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        form = form.save(commit=False).save()
        return super().form_valid(form)