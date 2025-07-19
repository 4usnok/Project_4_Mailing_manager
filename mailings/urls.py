from django.urls import path

from mailings.views import MainMailingsView

app_name = 'mailings'

urlpatterns = [
    path('', MainMailingsView.as_view(), name="mailings_list"),
    # path('forms/', ClientAddView.as_view(), name="forms_new_mail"),
]