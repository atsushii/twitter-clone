from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.LogInView.as_view(), name='log-in'),
    path('me/', views.ManageUserView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]