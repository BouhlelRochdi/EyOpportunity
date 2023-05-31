from django.db import models

# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    equipe = models.CharField(max_length=255)
    
    