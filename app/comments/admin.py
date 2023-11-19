from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "submit_date"]


admin.site.register(Comment, CommentAdmin)
