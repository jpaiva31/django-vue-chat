from auditlog.registry import auditlog
from django.db import models

from realmate_challenge.models import BaseModel


class Conversation(BaseModel):
    """Conversation model."""

    class State(models.TextChoices):
        """Conversation states."""

        OPEN = 'OPEN'
        CLOSED = 'CLOSED'

    state = models.CharField(
        max_length=6,
        choices=State.choices,
        default=State.OPEN,
        verbose_name="Estado"
    )

    class Meta:
        verbose_name = "Conversa"
        verbose_name_plural = "Conversas"
        ordering = ("created_at",)

    def __str__(self):
        """Return a string representation of the conversation."""
        return f"Conversation {self.id}"

    def close(self):
        """Close the conversation."""
        self.state = self.State.CLOSED
        self.save(update_fields=['state',])


auditlog.register(Conversation)