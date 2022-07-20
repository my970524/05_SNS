from django.contrib import admin

from .models import Post, Tag


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
