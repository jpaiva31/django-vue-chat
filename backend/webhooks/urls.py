from django.urls import path

from webhooks.views import WebhookMessageView

app_name = "webhooks"

urlpatterns = [
    path("", WebhookMessageView.as_view(), name="webhook_message"),
]