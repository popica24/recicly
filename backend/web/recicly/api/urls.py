from django.urls import path

from .views import PostsView

urlpatterns = [
    path('posts/', PostsView.as_view(), name="posts-list"),
    path('posts/<int:pk>/', PostsView.as_view(), name="posts-detail")
]