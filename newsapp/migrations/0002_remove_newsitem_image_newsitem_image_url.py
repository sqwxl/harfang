# Generated by Django 4.2.3 on 2023-07-05 16:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("newsapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="newsitem",
            name="image",
        ),
        migrations.AddField(
            model_name="newsitem",
            name="image_url",
            field=models.CharField(blank=True, max_length=400),
        ),
    ]