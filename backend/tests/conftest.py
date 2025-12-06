import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from chat_messages.models import Conversation


@pytest.fixture
def api_client():
    """Create an API client."""
    return APIClient()


@pytest.fixture
def admin_user():
    """Create an admin user."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123",
    )


@pytest.fixture
def conversation():
    """Create a conversation."""
    return Conversation.objects.create()