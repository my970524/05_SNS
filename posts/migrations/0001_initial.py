# Generated by Django 4.0.6 on 2022-07-21 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='태그이름')),
                ('slug', models.SlugField(allow_unicode=True, unique=True, verbose_name='태그슬러그')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제여부')),
                ('view_counts', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_posts', to=settings.AUTH_USER_MODEL, verbose_name='좋아요한 사람')),
                ('tags', models.ManyToManyField(blank=True, related_name='posts', to='posts.tag')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
    ]
