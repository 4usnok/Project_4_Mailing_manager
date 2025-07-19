from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('main_page.urls', namespace='main_page')),
    path('message/', include('message.urls', namespace='message')),
    path('client/', include('client.urls', namespace='client')),
    path('mailings/', include('mailings.urls', namespace='mailings')),
]
