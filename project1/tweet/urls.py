from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('tweet_list/', views.tweet_list, name='tweet_list'),
    path('tweet_create/', views.tweet_create, name='tweet_create'),
    path('tweet_update/<int:tweet_id>/', views.tweet_update, name='tweet_update'),
    path('tweet_delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]