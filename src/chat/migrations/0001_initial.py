# Generated by Django 4.2.11 on 2024-03-28 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=100, verbose_name='идентификатор')),
                ('source', models.CharField(choices=[('TG', 'Telegram'), ('WEB', 'Web')], max_length=3, verbose_name='источник')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='текст сообщения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата отправки')),
                ('is_user_message', models.BooleanField(default=True, verbose_name='отправлено пользователем')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatsession', verbose_name='сессия')),
            ],
        ),
    ]