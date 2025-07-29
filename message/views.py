from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, FormView, UpdateView, DeleteView, DetailView
from django.views.generic import ListView

from message.forms import MessageForm
from message.models import Message

@method_decorator(cache_page(60 * 15), name='dispatch')
class MainMessageView(LoginRequiredMixin, ListView):
    """ Просмотр страницы с сообщениями """
    model = Message
    template_name = "message/message_list_page.html"
    context_object_name = 'message_main'

    def get_queryset(self):
        """ низкоуровневое кэширование """
        queryset = cache.get('message_main')
        if not queryset:
            queryset = super().get_queryset()
            cache.get('message_main_queryset', queryset, 60 * 15)
        return queryset

class MessageAddView(CreateView):
    """ Добавление сообщений """
    model = Message
    fields = ['topic_mail',
            'body_mail',]
    template_name = "message/crud/form_message.html"
    success_url = reverse_lazy('message:messages_list')

class MessageUpdateView(UpdateView):
    """ Редактирование получателей """
    model = Message
    fields = ['topic_mail',
            'body_mail',]
    template_name = "message/crud/form_message.html"
    success_url = reverse_lazy('message:messages_list')

class MessageDeleteView(DeleteView):
    """ Удаление получателей """
    model = Message
    fields = ['topic_mail',
            'body_mail',]
    template_name = "message/crud/delete_message.html"
    success_url = reverse_lazy('message:messages_list')

@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageDetailView(DetailView):
    """ Подробная информация получателей """
    model = Message
    fields = ['topic_mail',
            'body_mail',]
    template_name = "message/crud/detail_message.html"
    success_url = reverse_lazy('message:messages_list')

@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageFormView(FormView):
    """ Форма для сообщений """
    form_class = MessageForm
    template_name = 'message/crud/form_message.html'
    success_url = reverse_lazy('message:messages_list')

    def form_valid(self, form):
        form = form.save(commit=False).save()
        return super().form_valid(form)
