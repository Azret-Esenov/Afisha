# Generated by Django 5.1.1 on 2024-09-09 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
