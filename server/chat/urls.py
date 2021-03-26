from django.urls import path, include
from chat import views

app_name = 'chat'

urlpatterns = [
    path('<str:username>/', views.ChatMessage.as_view(), name='chat')
]