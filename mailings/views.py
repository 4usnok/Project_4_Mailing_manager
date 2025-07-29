from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView, DetailView, TemplateView
from django.core.mail import send_mail
from mailings.forms import MailingsForm, MailingAttemptForm
from mailings.models import Newsletter


class MainMailingsView(LoginRequiredMixin, ListView):
    """ Просмотр страницы с сообщениями """
    model = Newsletter
    template_name = "mailings/mailings_list_page.html"
    context_object_name = 'mailings_context'

class MailMailingsView(FormView):
    """ Отправка на почту """
    form_class = MailingAttemptForm
    template_name = 'mailings/form_mailings.html'
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

class MailingsAddView(LoginRequiredMixin, CreateView):
    """ Добавление клиентов """
    model = Newsletter
    fields = [
        'status',
        'message',
        'recipients',
    ]
    template_name = "mailings/crud/form_mailings.html"
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)


class MailingsDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление клиентов """
    model = Newsletter
    fields = [
        'status',
        'message',
        'recipients',
    ]
    template_name = "mailings/crud/mailings_delete.html"
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_object(self, queryset=None):
        context = super().get_object(queryset)
        if context.owner != self.request.user:
            raise PermissionDenied("У вас нет прав редактировать эту анкету.")
        return context


class MailingsUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование клиентов """
    model = Newsletter
    fields = [
        'status',
        'message',
        'recipients',
    ]
    template_name = "mailings/crud/form_mailings.html"
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_object(self, queryset=None):
        context = super().get_object(queryset)
        if context.owner != self.request.user:
            raise PermissionDenied("У вас нет прав редактировать эту анкету.")
        return context

class MailingsDetailView(LoginRequiredMixin, DetailView):
    """ Подробная информация рассылки """
    model = Newsletter
    fields = [
        'status',
        'message',
        'recipients',
    ]
    template_name = "mailings/crud/detail_mailings.html"
    success_url = reverse_lazy('mailings:forms_detail')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

    def get_object(self, queryset=None):
        context = super().get_object(queryset)
        if (context.owner != self.request.user
                and not self.request.user.has_perm('mailings.can_view_for_manager')):
            raise PermissionDenied("У вас нет прав редактировать эту анкету.")
        return context


class MailingsFormView(FormView):
    """ Форма для клиента"""
    form_class = MailingsForm
    template_name = 'mailings/crud/form_mailings.html'
    success_url = reverse_lazy('mailings:mailings_list')

    def form_valid(self, form):
        form = form.save(commit=False).save()
        return super().form_valid(form)

class StaticsView(ListView):
    """ Просмотр страницы со статистикой """
    model = Newsletter
    template_name = "mailings/statics.html"
    context_object_name = 'mailings_context'

    def get_context_data(self, **kwargs):
        """ Отображение рассылок """
        context = super().get_context_data(**kwargs)
        queryset = Newsletter.objects.filter(owner=self.request.user) # Фильтр по владельцу

        # Пропишем переменные для обращения к моделям рассылок
        completed_count = queryset.filter(status="Завершена").count()
        unsuccessful_mailings = queryset.exclude(status="Завершена").count()
        context.update(
            {
                'successful_mailings': completed_count,  # успешные попытки рассылок
                'unsuccessful_mailings': unsuccessful_mailings,  # неуспешные попытки рассылок
                'sent_messages': completed_count,  # количество отправленных сообщений
            }
        )
        return context

class DisablingMailings(LoginRequiredMixin, View):
    """ Класс для отключения рассылки """
    model = Newsletter
    template_name = "mailings/dis_mailings.html"
    success_url = reverse_lazy('mailings:mailings_list')

    def post(self, request, pk):
        mailing_status = get_object_or_404(Newsletter, pk=pk)

        # Логика переключения статуса
        mailing_status.status = 'Завершена' if mailing_status.status == 'Создана' else 'Создана'
        mailing_status.save()
        return redirect(self.success_url)
