from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from config.permissions import IsOwnerOrReadOnly

from .models import Post
from .serializers import (
    DeletedPostListSerializer,
    PostCreateSerializer,
    PostDeleteSerializer,
    PostListSerializer,
    PostRestoreSerializer,
    PostUpdateSerializer,
)


# url : GET, POST /api/v1/posts
class PostListCreateView(generics.ListCreateAPIView):
    """
    게시글 목록보기, 게시글 생성 view 입니다.

    게시글 목록은 모든 유저가 볼 수 있지만,
    게시글 작성은 로그인 한 유저만 가능합니다.
    쿼리파라미터로 is_deleted=true를 받을 경우,
    삭제된 게시글 목록을 보여줍니다.
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
        if self.request.method == "GET" and self.request.GET:
            return DeletedPostListSerializer
        elif self.request.method == "GET":
            return PostListSerializer
        else:
            return PostCreateSerializer

    def list(self, request):
        """
        쿼리 파라미터로 is_deleted=true가 있는 경우,
        삭제된 게시글 목록을 보여줍니다.
        삭제된 게시글은 본인만 볼 수 있습니다.
        """
        if request.GET:
            if request.user.is_anonymous:
                return Response({"error": "접근권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
            queryset = Post.objects.filter(writer=request.user, is_deleted=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request):
        context = {"user": request.user}
        serializer = self.get_serializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "게시글 작성에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)


# url : GET, PUT, PATCH /api/v1/posts/<post_id>
class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateAPIView):
    """
    게시글 상세조회(GET), 수정(PUT), 삭제(PATCH) view 입니다.
    """

    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """HTTP 메소드에 따라 다른 queryset을 반환합니다."""
        if self.request.method == "PATCH":
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.filter(is_deleted=False)
        return queryset

    def get_serializer_class(self):
        """HTTP 메소드에 따라 다른 serializer를 반환합니다."""
        if self.request.method == "GET":
            return PostListSerializer
        elif self.request.method == "PUT":
            return PostUpdateSerializer
        else:
            return PostDeleteSerializer

    def retrieve(self, request, *args, **kwargs):
        """게시글을 상세 조회할 때마다 조회수가 1 증가합니다."""
        post = self.get_object()
        post.view_counts += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """부분수정도 가능하도록 partial_update를 지원합니다."""
        return self.partial_update(request, *args, **kwargs)


# url : PATCH /api/v1/posts/<post_id>/restore
class PostRestoreView(generics.UpdateAPIView):
    """
    삭제된 게시글 복구 view 입니다.
    """

    permission_classes = [IsOwnerOrReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostRestoreSerializer
