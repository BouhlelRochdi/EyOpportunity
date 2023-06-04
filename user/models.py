from django.db import models

# Create your models here.

class Equipe(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    equipeName = models.CharField(max_length=255)
    project= models.CharField(max_length=255, default='')


class EyUser(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    userName = models.CharField(max_length=255, )
    email = models.EmailField(max_length=255, unique=True, null=True)
    pwd = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, default='')
    type = models.CharField(max_length=255, null=True, blank=True)
    equipe = models.CharField(max_length=255, default='')
    activated = models.CharField(max_length=255, default='deactivated')
    access_token = models.CharField(max_length=255, default='')
    cv = models.FileField(upload_to='uploads/', default='')
    photo = models.FileField(upload_to='user/uploads/', default='')



class Archive(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    archiveName = models.CharField(max_length=255, null=True)
    dueDate= models.CharField(max_length=255, default='')
    file = models.FileField(upload_to='uploads/', default='')
    status = models.CharField(max_length=255, default='pending')
    progression = models.CharField(max_length=255, default='0%')
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, null=True)
    # def __init__(self, archiveName, archiveData, status, progression, id):
    #     self.archiveName = archiveName
    #     self.archiveData = archiveData
    #     self.status = status
    #     self.progression = progression
    #     self.id = id
        
    # def to_json(self):
    #     return {
    #         'archiveName': self.archiveName,
    #         'archiveData': self.archiveData,
    #         'status': self.status,
    #         'progression': self.progression,
    #         'id': self.id,
    #     }