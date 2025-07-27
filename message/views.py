from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, DeleteView, DetailView
from django.views.generic import ListView

from message.forms import MessageForm
from message.models import Message


class MainMessageView(ListView):
    """ Просмотр страницы с сообщениями """
    model = Message
    template_name = "message/message_list_page.html"
    context_object_name = 'message_main'

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

class MessageDetailView(DetailView):
    """ Подробная информация получателей """
    model = Message
    fields = ['topic_mail',
            'body_mail',]
    template_name = "message/crud/detail_message.html"
    success_url = reverse_lazy('message:messages_list')

class MessageFormView(FormView):
    """ Форма для сообщений """
    form_class = MessageForm
    template_name = 'message/crud/form_message.html'
    success_url = reverse_lazy('message:messages_list')

    def form_valid(self, form):
        form = form.save(commit=False).save()
        return super().form_valid(form)
