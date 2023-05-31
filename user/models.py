from django.db import models

# Create your models here.

class User(models.Model):
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    actors = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    duration = models.IntegerField()
    rate = models.IntegerField()
    userName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    equipe = models.CharField(max_length=255)
    
    