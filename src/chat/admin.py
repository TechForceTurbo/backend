from django.contrib import admin

from chat.models import ChatMessage, ChatSession, ContactInfo


class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 0


class ChatMessageInline(admin.StackedInline):
    model = ChatMessage
    extra = 0
    fields = ('message', 'created_at', 'is_user_message')
    readonly_fields = ('message', 'created_at', 'is_user_message')
    can_delete = False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'source', 'created_at')
    inlines = (ContactInfoInline, ChatMessageInline)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'message_preview',
                    'created_at', 'is_user_message')

    def message_preview(self, obj):
        return obj.message[:50]

    message_preview.short_description = 'Предпросмотр сообщения'
