from rest_framework import viewsets

from conversations.models import Conversation
from conversations.serializers import (
    ConversationReadSerializer,
    ConversationWriteSerializer,
)
from realmate_challenge.mixins import ReadWriteSerializerMixin


class ConversationViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    """Viewset for chat messages."""

    queryset = Conversation.objects.all()
    read_serializer_class = ConversationReadSerializer
    write_serializer_class = ConversationWriteSerializer
