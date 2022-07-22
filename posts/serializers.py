from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Post, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class PostListSerializer(ModelSerializer):
    """
    게시글 목록 보기에 사용되는 시리얼라이저 입니다.
    """

    writer = SerializerMethodField()
    tags = SerializerMethodField()

    def get_writer(self, obj):
        return obj.writer.username

    def get_tags(self, obj):
        tag_list = obj.tags.all()
        tag_name_list = []
        for tag in tag_list:
            tag_name = tag.name
            tag_name_list.append(tag_name)
        return tag_name_list

    class Meta:
        model = Post
        exclude = ["id", "updated_at", "is_deleted"]


class PostCreateSerializer(ModelSerializer):
    """
    게시글 생성에 사용되는 시리얼라이저 입니다.

    create 메소드를 오버라이딩 합니다.
    request body에서 받은 tags에 담긴 태그들이
    Tag 테이블에 존재하는지 확인하고, 없다면 생성하는 과정이 동반됩니다.
    """

    tags = TagSerializer(many=True)

    def create(self, validated_data):
        writer = self.context["user"]
        title = validated_data.get("title")
        content = validated_data.get("content")
        tags = validated_data.pop("tags")

        post = Post(
            writer=writer,
            title=title,
            content=content,
        )
        post.save()

        for t in tags:
            tag, created = Tag.objects.get_or_create(name=t["name"])
            post.tags.add(tag)

        return post

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
