from django.urls import path

from chat.views import ChatHistory

urlpatterns = [
    path('chat-history/<str:session_id>/', ChatHistory.as_view())
]
