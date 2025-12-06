from auditlog.registry import auditlog
from django.db import models

from conversations.models import Conversation
from realmate_challenge.models import BaseModel


class ChatMessage(BaseModel):
    """Chat message model."""

    class Direction(models.TextChoices):
        SENT = 'SENT'
        RECEIVED = 'RECEIVED'

    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE,
        verbose_name="Conversa",
    )
    direction = models.CharField(
        max_length=8,
        choices=Direction.choices,
        verbose_name="Direção",
    )
    content = models.TextField(verbose_name="Conteúdo")
    timestamp = models.DateTimeField(
        verbose_name="Horário",
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ('timestamp',)

    def __str__(self):
        """Return a string representation of the message."""
        return f'{self.direction}: {self.content}'

    @property
    def is_sent(self):
        """Return True if the message is sent."""
        return self.direction == self.Direction.SENT


auditlog.register(ChatMessage)