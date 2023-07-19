from django.contrib import admin

from news.models import Article, NewsSite, Submission


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "pub_date", "news_site"]
    list_filter = ["author", "news_site"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created_on", "flagged"]
    list_filter = ["user", "flagged"]


admin.site.register(NewsSite)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Submission, PostAdmin)
