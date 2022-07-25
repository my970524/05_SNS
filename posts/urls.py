from django.urls import path

from .views import PostLikeView, PostListCreateView, PostRestoreView, PostRetrieveUpdateDeleteView

urlpatterns = [
    path("posts", PostListCreateView.as_view(), name="post_list_create"),
    path("posts/<int:pk>", PostRetrieveUpdateDeleteView.as_view(), name="post_retrieve_update_delete"),
    path("posts/<int:pk>/restore", PostRestoreView.as_view(), name="post_restore"),
    path("posts/<int:pk>/like", PostLikeView.as_view(), name="post_like"),
]
