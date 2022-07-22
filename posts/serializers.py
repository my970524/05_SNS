from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Post, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class PostListSerializer(ModelSerializer):
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
