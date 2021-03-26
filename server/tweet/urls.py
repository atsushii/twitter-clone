from django.urls import path

from tweet import views

app_name = 'tweet'

urlpatterns = [
    path('create/', views.CreateTweetView.as_view(), name='create'),
    path('list/', views.TweetsListView.as_view(), name='list'),
    path('list/<int:tweet_id>', views.TweetDetailView.as_view(), name='detail'),
    path('update/<int:tweet_id>', views.TweetUpdateView.as_view(), name='update'),
    path('delete/<int:tweet_id>', views.TweetDeleteView.as_view(), name='delete'),
]