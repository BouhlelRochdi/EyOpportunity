from django.db import models

# Create your models here.

class EyUser(models.Model):
    userName = models.CharField(max_length=255, null=True, default = None)
    email = models.EmailField(null=False, default =None)
    password = models.CharField(max_length=255, null=True, blank=False, default = None)
    role = models.CharField(max_length=255, null=True, default = None)
    type = models.CharField(max_length=255, null=True, default = None)
    equipe = models.CharField(max_length=255, null=True, default = None)
    activated = models.CharField(max_length=255, default='checked')
    #def save(self, *args, **kwargs):
        #super(User, self).save(*args, **kwargs)
    

class Archive(models.Model):
    archiveName = models.CharField(max_length=255)
    archiveData = models.FileField()
    user = models.OneToOneField(EyUser, blank=True, null=True, on_delete=models.PROTECT) #oneToOne
    
    
    #models.ForeignKey(Author, on_delete=models.PROTECT, blank=False) ==> manyToOne
    #models.ManyToManyField(User) ==> manyToMany
    
    
class Equipe(models.Model):
    equipeName = models.CharField(max_length=255)
    #users = models.OneToOneField(User, on_delete=models.PROTECT, blank=False)