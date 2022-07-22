from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post
from .serializers import PostCreateSerializer, PostListSerializer


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Post.objects.filter(is_deleted=False)
        else:
            queryset = Post.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        else:
            return PostCreateSerializer

    def create(self, request):
        context = {"user": request.user}
        serializer = self.get_serializer(data=request.data, context=context)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "게시글 작성에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST)
