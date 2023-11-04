from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post, User

admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "pub_date", "publisher"]
    list_filter = ["author", "publisher"]


admin.site.register(Post, PostAdmin)
