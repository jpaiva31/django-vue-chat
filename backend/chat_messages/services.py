from django.core.exceptions import ValidationError

from chat_messages.models import ChatMessage
from conversations.models import Conversation


class ConversationService:
    """Serviço responsável pela criação, atualização,
    fechamento e validação de conversas e mensagens.
    """

    @staticmethod
    def new_conversation(data):
        """Cria uma nova conversa."""
        conversation_id = data.get("id")

        conversation, _ = Conversation.objects.get_or_create(
            id=conversation_id,
            defaults={"state": Conversation.State.OPEN},
        )

        return conversation

    @staticmethod
    def close_conversation(data):
        """Fecha uma conversa."""
        conversation_id = data.get("id")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist")

        conversation.close()

        return conversation

    @staticmethod
    def new_message(**data):
        """Cria uma nova mensagem."""
        msg_id = data.get("id")
        conversation_id = data.get("conversation_id")
        timestamp = data.get("timestamp")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist")

        if conversation.state == Conversation.State.CLOSED:
            raise ValidationError("Conversation is closed and cannot receive messages")

        msg, _ = ChatMessage.objects.update_or_create(
            id=msg_id,
            defaults={
                "conversation": conversation,
                "direction": data.get("direction"),
                "content": data.get("content"),
                "timestamp": timestamp,
            },
        )

        return msg
