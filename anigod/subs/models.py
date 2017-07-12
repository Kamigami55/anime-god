from django.db import models

# Create your models here.
class Anime(models.Model):
    name = models.CharField(max_length=50)
    volume = models.IntegerField(default=0)
    site = models.CharField(max_length=50)
    list_url = models.CharField(max_length=150)
    watch_url = models.CharField(max_length=150)
    img_url = models.CharField(max_length=150)
    img_src = models.CharField(max_length=150)
    subscribe = models.BooleanField()
    ended = models.BooleanField()
    def __str__(self):
        return '%s[%d]' % (self.name, self.volume)


class Comic(models.Model):
    name = models.CharField(max_length=50)
    volume = models.IntegerField(default=0)
    site = models.CharField(max_length=50)
    list_url = models.CharField(max_length=150)
    watch_url = models.CharField(max_length=150)
    img_url = models.CharField(max_length=150)
    img_src = models.CharField(max_length=150)
    subscribe = models.BooleanField()
    ended = models.BooleanField()
    def __str__(self):
        return '%s[%d]' % (self.name, self.volume)
