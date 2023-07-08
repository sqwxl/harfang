from django.contrib import admin

from newsapp.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "text", "created_on")
    list_filter = ("news_item", "user")
    search_fields = ("user__username", "news_item__title", "text")


admin.site.register(Comment, CommentAdmin)
