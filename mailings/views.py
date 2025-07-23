from itertools import count
from multiprocessing.connection import Client

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView, DetailView
from django.core.mail import send_mail

from mailings.forms import MailingsForm, MailingAttemptForm
from mailings.models import Newsletter



class MainMailingsView(ListView):
    """ Просмотр страницы с сообщениями """
    model = Newsletter
    template_name = "mailings/mailings_list_page.html"
    context_object_name = 'mailings_context'

class MailMailingsView(FormView):
    """ Отправка на почту """
    form_class = MailingAttemptForm
    template_name = 'mailings/form_mail_mailings.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        # Вызываем отправку письма
        dt_of_attempt = form.cleaned_data['dt_of_attempt']  # Передаём сообщение из формы
        status_of_attempt = form.cleaned_data['status_of_attempt']
        answer_server = form.cleaned_data['answer_server']

        subject = "Subject here"
        message = (f""
                   f"Дата и время попытки: {dt_of_attempt}\n"
                   f"Статус: {status_of_attempt}"
                   f"Ответ почтового сервера: {answer_server}\n"
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

class MailingsDetailView(DetailView):
    """ Подробная информация рассылки """
    model = Newsletter
    fields = '__all__'
    template_name = "mailings/crud/detail_mailings.html"
    success_url = reverse_lazy('mailings:forms_detail')

class MailingsFormView(FormView):
    """ Форма для клиента"""
    form_class = MailingsForm
    template_name = 'mailings/crud/form_mailings.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        form = form.save(commit=False).save()
        return super().form_valid(form)