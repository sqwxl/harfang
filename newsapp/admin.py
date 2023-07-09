from django.contrib import admin

from newsapp.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "text", "created_on", "edited_on", "deleted_on")
    list_filter = ("content_type", "user")
    search_fields = ("user__username", "content_type__title", "text")


admin.site.register(Comment, CommentAdmin)
