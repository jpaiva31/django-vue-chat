from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("messages/", include("chat_messages.urls")),
    path("conversations/", include("conversations.urls")),
    path("webhook/", include("webhooks.urls")),
]
