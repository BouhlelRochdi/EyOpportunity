from django.db import models

# Create your models here.

class Equipe(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    equipeName = models.CharField(max_length=255)
    equipeDesc = models.CharField(max_length=255, default='')

class EyUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    userName = models.CharField(max_length=255, )
    email = models.EmailField(null=False)
    pwd = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255)
    equipe = models.ForeignKey(Equipe, on_delete=models.PROTECT, null=True)  # manyToOne
    activated = models.CharField(max_length=255, default='deactivated')
    access_token = models.CharField(max_length=255, default='')


class Archive(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    archiveName = models.CharField(max_length=255)
    archiveData = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=255, default='pending')
    progression = models.CharField(max_length=255, default='0%')
    user = models.OneToOneField(EyUser, on_delete=models.PROTECT, default='')  # oneToOne
    equipe = models.OneToOneField(Equipe, on_delete=models.PROTECT, default='')  # oneToOne
