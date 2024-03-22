from django.db import models


class ChatMessage(models.Model):
    user_id = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_user_message = models.BooleanField(default=True)

    def __str__(self):
        return self.message

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['created_at'])
        ]
