from rest_framework import serializers

from chat_messages.serializers import ChatMessageReadSerializer
from conversations.models import Conversation


class ConversationReadSerializer(serializers.ModelSerializer):
    """ReadSerializer Conversation model."""

    messages = ChatMessageReadSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'messages', 'state',]


class ConversationWriteSerializer(serializers.ModelSerializer):
    """WriteSerializer Conversation model."""

    class Meta:
        model = Conversation
        fields = ['id']