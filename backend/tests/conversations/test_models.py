import pytest

from conversations.models import Conversation


@pytest.mark.django_db
def test_conversation_creation():
    """Test the creation of a conversation."""
    conversation = Conversation.objects.create()
    assert conversation.id is not None
    assert str(conversation) == f"Conversation {conversation.id}"
