# Generated by Django 4.0.6 on 2022-07-22 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='slug',
        ),
    ]