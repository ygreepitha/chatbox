from django.urls import path
from .views import ChatAPIView, YourViewFunction

urlpatterns = [
    path('api/chat/', ChatAPIView.as_view(), name='chat_api'),
    path('api/upload/', YourViewFunction, name='upload'),
]
