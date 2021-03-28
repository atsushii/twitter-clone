from django.urls import path, include
from chat import views

app_name = 'chat'

urlpatterns = [
    path('<str:username>/', views.TreadDetailView.as_view(), name='detail'),
    path('thread/list/', views.ThreadListView.as_view(), name='thread-list'),
    path('send/<str:username>/', views.SendMessageView.as_view(), name='send-message')
]