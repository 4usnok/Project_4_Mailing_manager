from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.views import UserRegisterView, UserConfirmEmailView, EmailConfirmationSentView, EmailConfirmedView, \
    EmailConfirmationFailedView

app_name = 'users'



urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(template_name="users/login_user.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page="main_page:main_view"), name="logout"),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    # сброс пароля:
    path('password_reset/',
         PasswordResetView.as_view(
        template_name="users/password_reset_form.html",
        email_template_name="users/password_reset_email.html",
        success_url=reverse_lazy("users:password_reset_done"),
        ),
         name="password_reset"

         ), # сброс пароля

    path('password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name="users/password_reset_done.html"
         ),
         name='password_reset_done'),

    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(
             template_name="users/password_reset_complete.html"
         ),
         name="password_reset_complete"),

    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html",
        success_url=reverse_lazy("users:password_reset_complete"),
         ),
         name="password_reset_confirm"), # временная ссылка на восстановление пароля
]