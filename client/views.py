from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, FormView, DeleteView, UpdateView, DetailView

from client.forms import ClientForm
from client.models import Recipient

@method_decorator(cache_page(60 * 15), name='dispatch')
class MainClientView(LoginRequiredMixin, ListView):
    """ Просмотр страницы с клиентами """
    model = Recipient
    template_name = "client/client_list_page.html"
    context_object_name = 'client_context'

    def get_queryset(self):
        """ низкоуровневое кэширование """
        queryset = cache.get('client_context_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.get('client_context_queryset', queryset, 60 * 15)
        return queryset

class ClientAddView(CreateView):
    """ Добавление клиентов """
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = "client/crud/form_client.html"
    success_url = reverse_lazy('client:client_list')

    def form_valid(self, form):
        """Присваивание владельца"""
        form.instance.owner = self.request.user  # Устанавливаем владельца
        return super().form_valid(form)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление клиентов """
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = "client/crud/client_delete.html"
    success_url = reverse_lazy('client:client_list')
    permission_required = 'client.delete_Recipient'

    def get_object(self, queryset=None):
        """ Установка прав доступа для владельца """
        context = super().get_object(queryset)
        if context.owner != self.request.user:
            raise PermissionDenied("У вас нет прав редактировать эту анкету.")
        return context

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование клиентов """
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = "client/crud/form_client.html"
    success_url = reverse_lazy('client:client_list')

    def get_object(self, queryset=None):
        """ Установка прав доступа для владельца """
        context = super().get_object(queryset)
        if context.owner != self.request.user:
            raise PermissionDenied("У вас нет прав редактировать эту анкету.")
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class ClientDetailView(LoginRequiredMixin, DetailView):
    """ Подробная информация клиентов """
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = "client/crud/client_detail.html"
    success_url = reverse_lazy('client:forms_detail')
    permission_required = 'client.view_Recipient'

    def get_object(self, queryset=None):
        """ Установка прав доступа для владельца """
        context = super().get_object(queryset)
        if (context.owner != self.request.user
            and not self.request.user.has_perm('client.can_view_for_manager')):
            raise PermissionDenied("У вас нет прав редактировать эту анкету.")
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class ClientFormView(FormView):
    """ Форма для клиента"""
    form_class = ClientForm
    template_name = 'client/crud/form_client.html'
    success_url = reverse_lazy('client:client_list')

    def form_valid(self, form):
        form = form.save(commit=False).save()
        return super().form_valid(form)
