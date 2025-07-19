from django.urls import path

from mailings.views import MainMailingsView, MailingsAddView, MailingsDeleteView, MailingsUpdateView

app_name = 'mailings'

urlpatterns = [
    path('', MainMailingsView.as_view(), name="mailings_list"),
    path('forms/', MailingsAddView.as_view(), name="forms_new_mail"),
    path('delete/<int:pk>', MailingsDeleteView.as_view(), name="forms_delete"),
    path('update/<int:pk>', MailingsUpdateView.as_view(), name="forms_update"),
]