from django.urls import path

from .views import PostListCreateView, PostRetrieveUpdateDeleteView

urlpatterns = [
    path("posts", PostListCreateView.as_view(), name="post_list_create"),
    path("posts/<int:pk>", PostRetrieveUpdateDeleteView.as_view(), name="post_retrieve_update"),
]
