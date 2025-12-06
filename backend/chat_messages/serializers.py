from rest_framework import serializers

from chat_messages.models import ChatMessage


class ChatMessageReadSerializer(serializers.ModelSerializer):
    """Read serializer for ChatMessage model."""

    direction = serializers.CharField(source='get_direction_display')

    class Meta:
        model = ChatMessage
        fields = [
            'conversation', 'direction', 'content',
            'timestamp',
        ]


class ChatMessageWriteSerializer(serializers.ModelSerializer):
    """Write serializer for ChatMessage model."""

    class Meta:
        model = ChatMessage
        fields = [
            'id', 'conversation', 'direction',
            'content', 'timestamp'
        ]


class WebhookSerializer(serializers.Serializer):
    """Serializer for webhook data."""

    type = serializers.ChoiceField(
        choices=["NEW_CONVERSATION", "NEW_MESSAGE", "CLOSE_CONVERSATION"]
    )
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()

    def validate(self, attrs):
        """Validates the webhook data."""
        event_type = attrs["type"]
        data = attrs["data"]

        if event_type == "NEW_CONVERSATION":
            if "id" not in data:
                raise serializers.ValidationError({
                    "data": "Conversation id is required."
                })

        elif event_type == "NEW_MESSAGE":
            required = ["id", "conversation_id", "direction", "content"]
            missing = [f for f in required if f not in data]

            if missing:
                raise serializers.ValidationError({
                    "data": f"Missing fields: {', '.join(missing)}"
                })

            if data["direction"] not in ["SENT", "RECEIVED"]:
                raise serializers.ValidationError({"data": "Invalid direction."})

        elif event_type == "CLOSE_CONVERSATION":
            if "id" not in data:
                raise serializers.ValidationError(
                    {"data": "Conversation id is required."}
                )

        return attrs