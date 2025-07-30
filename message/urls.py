from django.urls import path

from message.views import MainMessageView, MessageFormView, MessageUpdateView, MessageDeleteView, MessageDetailView

app_name = 'message'

urlpatterns = [
    path('', MainMessageView.as_view(), name="messages_list"),
    path('forms/', MessageFormView.as_view(), name="forms_new_message"),
    path('update/<int:pk>', MessageUpdateView.as_view(), name="forms_update"),
    path('delete/<int:pk>', MessageDeleteView.as_view(), name="forms_delete"),
    path('detail/<int:pk>', MessageDetailView.as_view(), name="forms_detail"),
]