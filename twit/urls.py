from django.urls import path

from . import views

app_name = 'twit'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/comment/', views.CommentView.as_view(), name='comment'),
    path('<int:tweet_id>/commenting/', views.commenting, name='commenting'),
    path('<int:tweet_id>/translating/', views.translating, name='translating'),
]
