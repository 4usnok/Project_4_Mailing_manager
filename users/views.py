from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


from users.forms import UserRegistrationForm


@method_decorator(cache_page(60 * 15), name='dispatch')
class UserListView(ListView):
    """ Класс для просмотра списка пользователей """
    model=User
    template_name='users/users_list.html'
    context_object_name = 'users_context'

    def get_queryset(self):
        """ низкоуровневое кэширование """
        queryset = cache.get('users_context')
        if not queryset:
            queryset = super().get_queryset()
            cache.get('users_context_queryset', queryset, 60 * 15)
        return queryset

class UserRegisterView(SuccessMessageMixin, CreateView):
    """ Класс для регистрации """
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")
    form_class = UserRegistrationForm
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user) # Создание токена
        uid = urlsafe_base64_encode(force_bytes(user.pk)) # Кодирование токена
        activation_url = reverse("users:confirm_email", kwargs={'uidb64': uid, 'token': token}) # Перенаправление на страницу
        current_site = 'localhost:8000'
        # содержание письма
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            'chusnok25@yandex.ru',
            [user.email],
            fail_silently=False,
        )
        return redirect("users:email_confirmation_sent") # перенаправление при успехе

class UserConfirmEmailView(View):
    """ Обработка запроса на активацию аккаунта """
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')

class EmailConfirmationSentView(TemplateView):
    """ Успешный запрос на подтверждение """
    template_name = 'users/registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context

class EmailConfirmedView(TemplateView):
    """ Окончание подтверждения """
    template_name = 'users/registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context

class EmailConfirmationFailedView(TemplateView):
    """ Ошибка в токен-ссылке """
    template_name = 'users/registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class UserBlock(LoginRequiredMixin, TemplateView):
    """ Класс для блокировки юзера """
    template_name='users/user_block_status.html'

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_active == True:
            user.is_active = False
        elif user.is_active == False:
            user.is_active = True
        user.save()
        return redirect('users:users_list')
