import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_message(api_client, conversation):
    """Test the create message view."""
    url = reverse("chat_messages:chat_messages-list")

    payload = {
        "direction": "RECEIVED",
        "content": "Olá! Tudo bem?",
        "conversation": str(conversation.id),
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert response.data["content"] == payload["content"]
