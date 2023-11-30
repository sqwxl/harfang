from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "submit_date"]
    list_filter = ["user"]


admin.site.register(Post, PostAdmin)
