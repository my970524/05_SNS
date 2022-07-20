from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import User


# Register your models here.
class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("id", "email", "username", "is_admin")
    list_filter = ("is_admin",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal_info", {"fields": ("username",)}),
        ("Permissions", {"fields": ("is_admin",)}),
        ("Datetime_info", {"fields": ("date_joined", "updated_at")}),
    )

    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "username", "password1", "password2")}),)

    filter_horizontal = ()

    readonly_fields = ["date_joined", "updated_at"]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
