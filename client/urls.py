from django.urls import path

from client.views import MainClientView, ClientAddView

app_name = 'message'

urlpatterns = [
    path('', MainClientView.as_view(), name="client_list"),
    path('forms/', ClientAddView.as_view(), name="forms_new_client"),
]