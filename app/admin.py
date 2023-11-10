from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post, User

admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "submit_date"]
    list_filter = ["user"]


admin.site.register(Post, PostAdmin)
