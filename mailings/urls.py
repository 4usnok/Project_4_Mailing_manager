from django.urls import path

from mailings import views
from mailings.views import MainMailingsView, MailingsAddView, MailingsDeleteView, MailingsUpdateView, MailMailingsView

app_name = 'mailings'

urlpatterns = [
    path('', MainMailingsView.as_view(), name="mailings_list"),
    path('mail/', MailMailingsView.as_view(), name="mail"),
    path('forms/', MailingsAddView.as_view(), name="forms_new_mail"),
    path('delete/<int:pk>', MailingsDeleteView.as_view(), name="forms_delete"),
    path('update/<int:pk>', MailingsUpdateView.as_view(), name="forms_update"),
]