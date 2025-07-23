from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegistrationForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    """ Функция для регистрации """
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")
    form_class = UserRegistrationForm
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context