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


class ContactInfo(models.Model):
    """
    Модель для хранения контактной информации пользователя в чате.
    Содержит имя пользователя, его номер телефона и связь с сессией чата.
    """
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='contact_info',
        verbose_name='Сессия'
    )

    def __str__(self):
        return f'{self.name} ({self.phone})'
