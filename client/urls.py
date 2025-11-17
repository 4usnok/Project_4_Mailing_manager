from django.urls import path

from client.views import MainClientView, ClientAddView, ClientDeleteView, ClientUpdateView, ClientDetailView

app_name = 'client'

urlpatterns = [
    path('', MainClientView.as_view(), name="client_list"),
    path('forms/', ClientAddView.as_view(), name="forms_new_client"),
    path('detail/<int:pk>', ClientDetailView.as_view(), name="forms_detail"),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name="forms_delete"),
    path('update/<int:pk>', ClientUpdateView.as_view(), name="forms_update"),
]