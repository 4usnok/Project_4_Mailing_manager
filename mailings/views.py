from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView
from django.core.mail import send_mail
from pyexpat.errors import messages

from mailings.forms import MailingsForm
from mailings.models import Newsletter


class MainMailingsView(ListView):
    """ Просмотр страницы с сообщениями """
    model = Newsletter
    template_name = "mailings/mailings_list_page.html"
    context_object_name = 'mailings_context'

class MailMailingsView(FormView):
    """ Отправка на почту """
    form_class = MailingsForm
    template_name = 'mailings/form_mail_mailings.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        # Вызываем отправку письма
        message_text = form.cleaned_data['message']  # Передаём сообщение из формы
        recipients_text = form.cleaned_data['recipients']
        status_text = form.cleaned_data['status']

        subject = "Subject here"
        message = (f""
                   f"сообщение: {message_text}\n"
                   f"получатели: {recipients_text}"
                   f"статус: {status_text}\n"
                   )
        from_mail = "chusnok25@yandex.ru"
        recipient_list = ["chusnok25@yandex.ru"]
        send_mail(subject, message, from_mail, recipient_list)

        return super().form_valid(form)  # Перенаправляем на success_url

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