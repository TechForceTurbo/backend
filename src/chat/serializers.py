from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from chat.models import ChatMessage, ContactInfo, ChatSession


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'message', 'created_at', 'is_user_message')


class ContactInfoSerializer(serializers.ModelSerializer):
    session_uuid = serializers.UUIDField(
        write_only=True,
        source='session.session_id'
    )

    class Meta:
        model = ContactInfo
        fields = ['name', 'phone', 'session_uuid']

    def create(self, validated_data):
        session_id = validated_data.pop('session')['session_id']
        session = get_object_or_404(ChatSession, session_id=session_id)
        contact_info = ContactInfo.objects.create(**validated_data,
                                                  session=session)
        return contact_info
