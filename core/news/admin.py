from django.contrib import admin
from news.models import Article, NewsSite


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "pub_date", "news_site"]
    list_filter = ["author", "news_site"]


admin.site.register(NewsSite)
admin.site.register(Article, ArticleAdmin)
