from django.contrib import admin

from newsapp.models import Article, ArticleComment, NewsSite, Submission, SubmissionComment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "pub_date", "news_site"]
    list_filter = ["author", "news_site"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created_on", "flagged"]
    list_filter = ["user", "flagged"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "text", "created_on"]
    list_display_links = ["text"]
    list_filter = ["user", "flagged"]


admin.site.register(NewsSite)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Submission, PostAdmin)
admin.site.register(SubmissionComment, CommentAdmin)
admin.site.register(ArticleComment, CommentAdmin)
