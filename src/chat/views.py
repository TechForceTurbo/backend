from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import ChatSession
from chat.serializers import ChatMessageSerializer


class ChatHistory(APIView):
    def get(self, request, session_id):
        session = get_object_or_404(ChatSession, session_id=session_id)
        messages = session.messages.all().order_by('-created_at')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
