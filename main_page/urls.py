from django.urls import path

from main_page.views import MainView

app_name = 'main_page'

urlpatterns = [
    path('', MainView.as_view(), name="main_view"),
]