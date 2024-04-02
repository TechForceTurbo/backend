from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from chat.models import ChatSession
from chat.serializers import ChatMessageSerializer


class ChatHistory(GenericAPIView, ListModelMixin):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        session = get_object_or_404(ChatSession, session_id=session_id)
        return session.messages.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)