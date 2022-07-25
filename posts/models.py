from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField("태그이름", max_length=50)
    # slug = models.SlugField("태그슬러그", max_length=50, unique=True, allow_unicode=True, null=True)

    def __str__(self):
        return f"id: {self.pk}/ {self.name}"


class Post(models.Model):
    title = models.CharField("제목", max_length=200)
    content = models.TextField("내용")
    writer = models.ForeignKey(to=User, verbose_name="작성자", on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(to=Tag, blank=True, related_name="posts")
    created_at = models.DateTimeField("작성일자", auto_now_add=True)
    updated_at = models.DateTimeField("수정일자", auto_now=True)
    is_deleted = models.BooleanField("삭제여부", default=False)
    view_counts = models.PositiveIntegerField("조회수", default=0)
    like_users = models.ManyToManyField(to=User, verbose_name="좋아요한 사람", related_name="like_posts", blank=True)

    def __str__(self):
        return f"id: {self.pk}/ title: {self.title}"
