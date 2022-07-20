# Generated by Django 4.0.6 on 2022-07-20 20:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='like_posts', to=settings.AUTH_USER_MODEL, verbose_name='좋아요한 사람'),
        ),
        migrations.AddField(
            model_name='post',
            name='view_counts',
            field=models.PositiveIntegerField(default=0, verbose_name='조회수'),
        ),
    ]