import pytest

from chat_messages.serializers import ChatMessageWriteSerializer


@pytest.mark.django_db
def test_write_message_serializer_valid(conversation):
    """Test the write message serializer."""
    data = {
        "content": "Olá!",
        "direction": "RECEIVED",
        "conversation": conversation.id,
    }

    serializer = ChatMessageWriteSerializer(data=data)

    assert serializer.is_valid(), serializer.errors
