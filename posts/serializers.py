from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Post, Tag


class TagBaseSerializer(ModelSerializer):
    """
    Tag모델의 기본 시리얼라이저 입니다.
    """

    class Meta:
        model = Tag
        fields = ["name"]


class PostBaseSerializer(ModelSerializer):
    """
    Post모델의 기본 시리얼라이저 입니다.
    """

    writer = SerializerMethodField()
    tags = SerializerMethodField()
    like_count = SerializerMethodField()
    like_users = SerializerMethodField()

    def get_writer(self, obj):
        return obj.writer.username

    def get_tags(self, obj):
        tag_list = obj.tags.all()
        tag_name_list = []
        for tag in tag_list:
            tag_name = tag.name
            tag_name_list.append(tag_name)
        return tag_name_list

    def get_like_count(self, obj):
        like_count = obj.like_users.count()
        return like_count

    def get_like_users(self, obj):
        like_users_list = obj.like_users.all()
        result = []
        for user in like_users_list:
            result.append({"id": user.id, "username": user.username})
        return result

    class Meta:
        model = Post
        exclude = ["is_deleted"]


class PostListSerializer(PostBaseSerializer):
    """
    게시글 목록 보기에 사용되는 시리얼라이저 입니다.
    PostBaseSerializer를 상속받습니다.
    """

    pass


class DeletedPostListSerializer(PostBaseSerializer):
    """
    삭제된 게시글 목록 보기에 사용되는 시리얼라이저 입니다.
    PostBaseSerializer를 상속받습니다.
    is_deleted를 포함한 모든 필드를 직렬화 합니다.
    """

    class Meta(PostBaseSerializer.Meta):
        exclude = []


class PostCreateSerializer(ModelSerializer):
    """
    게시글 생성에 사용되는 시리얼라이저 입니다.

    create 메소드를 오버라이딩 합니다.
    request body에서 받은 tags에 담긴 태그들이
    Tag 테이블에 존재하는지 확인하고, 없다면 생성하는 과정이 동반됩니다.
    """

    tags = TagBaseSerializer(many=True)

    def create(self, validated_data):
        writer = self.context["user"]
        tags = validated_data.pop("tags")

        post = Post.objects.create(writer=writer, **validated_data)
        post.save()

        if tags:
            for t in tags:
                tag, created = Tag.objects.get_or_create(name=t["name"])
                post.tags.add(tag)

        return post

    class Meta:
        model = Post
        fields = ["id", "title", "content", "tags"]


class PostUpdateSerializer(PostCreateSerializer):
    """
    게시글 수정에 사용되는 시리얼라이저 입니다.
    PostCreateSerializer를 상속받습니다.

    update 메소드를 오버라이딩 합니다.
    request body에서 받은 태그들로 게시글의 태그들이 교체 됩니다.
    ex)
    기존 태그 => #파이썬, #장고
    request body => #drf
    바뀐 태그 => #drf
    """

    tags = TagBaseSerializer(many=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()

        tags = validated_data.pop("tags", [])
        if tags:
            tag_objs = []
            for t in tags:
                tag, created = Tag.objects.get_or_create(name=t["name"])
                tag_objs.append(tag)
            instance.tags.set(tag_objs)

        return instance


class PostDeleteSerializer(PostBaseSerializer):
    """
    게시글 삭제에 사용되는 시리얼라이저 입니다.
    PostBaseSerializer를 상속받습니다.
    is_deleted 필드 값을 True로 수정합니다.
    """

    tags = TagBaseSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        if instance.is_deleted == True:
            raise serializers.ValidationError("이 게시글은 이미 삭제되었습니다.")
        instance.is_deleted = True
        instance.save()
        return instance

    class Meta(PostBaseSerializer.Meta):
        exclude = []


class PostRestoreSerializer(PostDeleteSerializer):
    """
    삭제된 게시글 복구에 사용되는 시리얼라이저 입니다.
    PostDeleteSerializer를 상속받습니다.
    is_deleted 필드 값을 False로 수정합니다.
    """

    def update(self, instance, validated_data):
        if instance.is_deleted == False:
            raise serializers.ValidationError("이 게시글은 삭제된 게시글이 아닙니다.")
        instance.is_deleted = False
        instance.save()
        return instance


class PostLikeSerializer(PostBaseSerializer):
    """
    게시글 좋아요에 사요되는 시리얼라이저 입니다.
    PostBaseSerializer를 상속받습니다.
    """

    def update(self, instance, validated_data):
        like_users = instance.like_users.all()
        user = self.context["user"]
        if user in like_users:
            raise serializers.ValidationError("이미 좋아요를 했습니다.")
        instance.like_users.add(user)
        instance.save()
        return instance


class PostUnlikeSerializer(PostBaseSerializer):
    """
    게시글 좋아요 취소에 사용되는 시리얼라이저 입니다.
    PostBaseSerializer를 상속받습니다.
    """

    def update(self, instance, validated_data):
        like_users = instance.like_users.all()
        user = self.context["user"]
        if user not in like_users:
            raise serializers.ValidationError("좋아요를 하지 않은 게시글로 좋아요를 취소할 수 없습니다.")
        instance.like_users.remove(user)
        instance.save()
        return instance
