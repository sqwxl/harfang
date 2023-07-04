from django.db import models


class NewsSite(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    rss_url = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logos/", blank=True)

    def __str__(self):
        return self.name


class NewsItem(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="Unknown")
    source_url = models.CharField(max_length=200)
    date = models.DateTimeField("date published")
    text = models.TextField()
    news_site = models.ForeignKey("NewsSite", on_delete=models.CASCADE)
