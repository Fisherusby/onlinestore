from django.conf import settings
from django.db import models


class Forum(models.Model):
    title = models.CharField(max_length=64, verbose_name="Тема форума")
    icon = models.ImageField(verbose_name="Icon", blank=True, null=True)


class Topic(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=128, verbose_name="Тема")
    # description = models.CharField(max_length=255, verbose_name='Краткое описание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Автор")
    creation_date = models.DateTimeField(auto_now=True)


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="posts")
    text_of_post = models.CharField(max_length=1024, verbose_name="Пост")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="Автор")
    creation_date = models.DateTimeField(auto_now=True)
    edit_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL)
