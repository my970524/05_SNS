from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post
from .serializers import PostCreateSerializer, PostListSerializer, PostUpdateSerializer


# url : GET, POST /api/v1/posts
class PostListCreateView(generics.ListCreateAPIView):
    """
    게시글 목록보기, 게시글 생성 view 입니다.

    게시글 목록은 모든 유저가 볼 수 있지만,
    게시글 작성은 로그인 한 유저만 가능합니다.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """HTTP 메소드에 따라 다른 queryset을 반환합니다."""
        if self.request.method == "GET":
            queryset = Post.objects.filter(is_deleted=False)
        else:
            queryset = Post.objects.all()
        return queryset

    def get_serializer_class(self):
        """HTTP 메소드에 따라 다른 serializer를 반환합니다."""
        if self.request.method == "GET":
            return PostListSerializer
        else:
            return PostCreateSerializer

    def create(self, request):
        context = {"user": request.user}
        serializer = self.get_serializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "게시글 작성에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)


# url : GET, PUT, PATCH /api/v1/posts/<post_id>
class PostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    게시글 상세조회, 수정, 삭제(soft delete) view 입니다.
    """

    queryset = Post.objects.all()

    def get_serializer_class(self):
        """HTTP 메소드에 따라 다른 serializer를 반환합니다."""
        if self.request.method == "GET":
            return PostListSerializer
        else:
            return PostUpdateSerializer

    def put(self, request, *args, **kwargs):
        """부분수정도 가능하도록 partial_update를 지원합니다."""
        return self.partial_update(request, *args, **kwargs)
