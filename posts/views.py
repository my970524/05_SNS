from django.core.paginator import Paginator
from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from config.permissions import IsOwnerOrReadOnly

from .models import Post
from .serializers import (
    DeletedPostListSerializer,
    PostCreateSerializer,
    PostDeleteSerializer,
    PostLikeSerializer,
    PostListSerializer,
    PostRestoreSerializer,
    PostUnlikeSerializer,
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

        검색 : 키워드를 제목 or 내용에서 포함하는 게시글 검색
        - parameter : search
        필터 : 키워드를 태그로 가지고 있는 게시글 필터
        - parameter : tags
        정렬 : 작성일, 좋아요 수, 조회수 기준으로 정렬
        - parameter : order
        페이지네이션 : default는 게시글 5개씩, 첫 번째 페이지 반환
        - parameter :page_counts(한 페이지 게시글 개수), page_num(보여주는 페이지 번호)
        """
        if request.GET.get("is_deleted"):
            if request.user.is_anonymous:
                return Response({"error": "접근권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
            queryset = Post.objects.filter(writer=request.user, is_deleted=True)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            objs = self.get_queryset()
            """게시글 제목, 내용에서 검색"""
            search = request.GET.get("search")
            if search:
                objs = objs.filter(Q(title__icontains=search) | Q(content__icontains=search))

            """게시글 태그 필터링"""
            tags = request.GET.get("tags")
            if tags:
                tags = tags.split(",")
                objs = objs.filter(tags__name__in=tags)

            """게시글 정렬 (작성일, 좋아요 수, 조회수 중 택 1 기준)"""
            order = request.GET.get("order")
            if order:
                if order == "asc":
                    objs = objs.order_by("created_at", "id")
                elif order == "desc":
                    objs = objs.order_by("-created_at", "id")
                elif order == "likes_asc":
                    objs = objs.annotate(likes=Count("like_users")).order_by("likes", "id")
                elif order == "likes_desc":
                    objs = objs.annotate(likes=Count("like_users")).order_by("-likes", "id")
                elif order == "views_asc":
                    objs = objs.order_by("view_counts", "id")
                elif order == "views_desc":
                    objs = objs.order_by("-view_counts", "id")

            """게시글 페이지네이션"""
            page_counts = request.GET.get("page_counts", 5)
            page_num = request.GET.get("page_num", 1)
            paginator = Paginator(objs, page_counts)

            serializer = self.get_serializer(paginator.get_page(page_num), many=True)
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
        queryset = Post.objects.filter(is_deleted=False, pk=self.kwargs["pk"])
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

    def get_queryset(self):
        queryset = Post.objects.filter(is_deleted=True, pk=self.kwargs["pk"])
        return queryset

    serializer_class = PostRestoreSerializer


# url : PATCH /api/v1/posts/<post_id>/like
class PostLikeView(generics.UpdateAPIView):
    """
    게시글 좋아요 view 입니다.
    로그인 한 유저만 좋아요를 할 수 있습니다.
    이미 좋아요를 한 경우는 시리얼라이저에서 예외처리 됩니다.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(is_deleted=False, pk=self.kwargs["pk"])
        return queryset

    serializer_class = PostLikeSerializer

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        context = {"user": request.user}
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, context=context, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "이 포스트에 좋아요를 눌렀습니다."})


# url : PATCH /api/v1/posts/<post_id>/unlike
class PostUnlikeView(generics.UpdateAPIView):
    """
    게시글 좋아요 취소 view 입니다.
    로그인 한 유저만 좋아요를 취소할 수 있습니다.
    좋아요를 하지 않았거나, 이미 취소된 경우는 시리얼라이저에서 예외처리 됩니다.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(is_deleted=False, pk=self.kwargs["pk"])
        return queryset

    serializer_class = PostUnlikeSerializer

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        context = {"user": request.user}
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, context=context, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "이 포스트에 대한 좋아요를 취소했습니다."})
