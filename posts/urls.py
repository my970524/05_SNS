from django.urls import path

from .views import PostListCreateView, PostRetrieveUpdateView

urlpatterns = [
    path("posts", PostListCreateView.as_view(), name="post_list_create"),
    path("posts/<int:pk>", PostRetrieveUpdateView.as_view(), name="post_retrieve_update"),
]
