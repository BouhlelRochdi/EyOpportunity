from django.db import models

# Create your models here.

class EyUser(models.Model):
    id = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=255, )
    email = models.EmailField(null=False)
    pwd = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255)
    equipe = models.CharField(max_length=255)
    activated = models.CharField(max_length=255, default='deactivated')
    access_token= models.CharField(max_length=255)
    #def save(self, *args, **kwargs):
        #super(User, self).save(*args, **kwargs)
    

class Archive(models.Model):
    id = models.AutoField(primary_key=True)
    archiveName = models.CharField(max_length=255)
    archiveData = models.FileField(upload_to='uploads/')
    user = models.OneToOneField(EyUser, blank=True, null=True, on_delete=models.PROTECT) #oneToOne
    
    
    #models.ForeignKey(Author, on_delete=models.PROTECT, blank=False) ==> manyToOne
    #models.ManyToManyField(User) ==> manyToMany
    
    
class Equipe(models.Model):
    id = models.AutoField(primary_key=True)
    equipeName = models.CharField(max_length=255)
    #users = models.OneToOneField(User, on_delete=models.PROTECT, blank=False)