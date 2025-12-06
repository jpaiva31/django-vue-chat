from rest_framework.routers import DefaultRouter

from chat_messages.views import ChatMessageViewSet

app_name = "chat_messages"

router = DefaultRouter()
router.register("", ChatMessageViewSet, basename="chat_messages")

urlpatterns = router.urls
