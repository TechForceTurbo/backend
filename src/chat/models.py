from django.db import models


class ChatSession(models.Model):
    """
    Модель сессии чата. Сессия может исходить от различных источников
    и содержит информацию о времени её создания и последнего обновления.
    """
    SOURCE_CHOICES = [
        ('TG', 'Telegram'),
        ('WEB', 'Web'),
    ]
    session_id = models.CharField(max_length=100, verbose_name='идентификатор')
    source = models.CharField(
        max_length=3,
        choices=SOURCE_CHOICES,
        verbose_name='источник'
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='дата создания')


class ChatMessage(models.Model):
    """
    Модель сообщения в сессии чата. Связано с моделью ChatSession и содержит
    информацию о тексте сообщения, его отправителе и времени отправки.
    """
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        db_index=True,
        verbose_name='сессия'
    )
    message = models.TextField(verbose_name='текст сообщения')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='дата отправки')
    is_user_message = models.BooleanField(
        default=True,
        verbose_name='отправлено пользователем'
    )