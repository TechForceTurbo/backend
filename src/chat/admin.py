from django.contrib import admin
from chat.models import ChatMessage, ChatSession

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass