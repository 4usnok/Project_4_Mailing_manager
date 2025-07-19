from django.urls import path

from client.views import MainClientView, ClientAddView, ClientDeleteView, ClientUpdateView

app_name = 'message'

urlpatterns = [
    path('', MainClientView.as_view(), name="client_list"),
    path('forms/', ClientAddView.as_view(), name="forms_new_client"),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name="forms_delete"),
    path('update/<int:pk>', ClientUpdateView.as_view(), name="forms_update"),

]