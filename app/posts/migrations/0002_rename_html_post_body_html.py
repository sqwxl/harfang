# Generated by Django 5.0 on 2023-12-10 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='html',
            new_name='body_html',
        ),
    ]
