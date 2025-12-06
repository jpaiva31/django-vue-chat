from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat_messages.serializers import WebhookSerializer
from chat_messages.services import ConversationService


class WebhookMessageView(APIView):
    """Webhook view for processing messages."""

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """Process a webhook message."""
        event_type = request.data.get("type")
        timestamp = request.data.get("timestamp")
        data = request.data.get("data", {}) or {}

        serializer = WebhookSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            if event_type == "NEW_CONVERSATION":
                conversation = ConversationService.new_conversation(data)
                return Response(
                    {"status": "conversation_created", "id": str(conversation.id)},
                    status=status.HTTP_201_CREATED
                )

            elif event_type == "NEW_MESSAGE":
                msg = ConversationService.new_message(**data, timestamp=timestamp)
                return Response(
                    {"status": "message_created", "id": str(msg.id)},
                    status=status.HTTP_201_CREATED
                )

            elif event_type == "CLOSE_CONVERSATION":
                conversation = ConversationService.close_conversation(data)
                return Response(
                    {"status": "conversation_closed", "id": str(conversation.id)},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {"error": f"Unknown event type '{event_type}'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": "Internal server error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )