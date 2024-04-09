from django.urls import path

from chat.views import ChatHistory, ContactInfoView

urlpatterns = [
    path('chat-history/<str:session_id>/', ChatHistory.as_view()),
    path('contact-info/', ContactInfoView.as_view())
]
