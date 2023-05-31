from django.db import models

# Create your models here.

class User(models.Model):
    userName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    equipe = models.CharField(max_length=255)
    activated = models.BooleanField()
    

class Archive(models.Model):
    archiveName = models.CharField(max_length=255)
    archiveData = models.FileField()
    #user = models.OneToOneField(User, blank=True, null=True) #oneToOne
    
    
    #models.ForeignKey(Author, on_delete=models.PROTECT, blank=False) ==> manyToOne
    #models.ManyToManyField(User) ==> manyToMany
    
    
class Equipe(models.Model):
    equipeName = models.CharField(max_length=255)
    #users = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)