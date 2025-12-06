from rest_framework import viewsets

from chat_messages.models import ChatMessage
from chat_messages.serializers import (
    ChatMessageReadSerializer,
    ChatMessageWriteSerializer,
)
from realmate_challenge.mixins import ReadWriteSerializerMixin


class ChatMessageViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """Viewset for chat messages."""

    queryset = ChatMessage.objects.all()
    read_serializer_class = ChatMessageReadSerializer
    write_serializer_class = ChatMessageWriteSerializer
