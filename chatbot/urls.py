from django.urls import path
from .views import ChatbotView, ChatbotRecommendView

urlpatterns = [
    path('chat/', ChatbotView.as_view(), name='chatbot'),
    path('recommend/', ChatbotRecommendView.as_view(), name='chatbot-recommend'),
]