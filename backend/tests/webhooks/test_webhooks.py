import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_new_message_webhook(api_client, conversation):
    """Test the new message webhook."""
    url = reverse("webhooks:webhook_message")

    payload = {
        "type": "NEW_MESSAGE",
        "timestamp": "2025-02-21T10:20:42.349308",
        "data": {
            "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
            "direction": "RECEIVED",
            "content": "Olá, tudo bem?",
            "conversation_id": conversation.id
        }
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
