from django.db import models

# Create your models here.

class Equipe(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    equipeName = models.CharField(max_length=255)
    project= models.CharField(max_length=255, default='')
    
    # def __init__(self, equipeName, equipeDesc, id):
    #     self.equipeName = equipeName
    #     self.equipeDesc = equipeDesc
    #     self.id = id

    # def to_json(self):
    #     return {
    #         'equipeName': self.equipeName,
    #         'equipeDesc': self.equipeDesc,
    #         'id': self.id,
    #     }

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
    # def __init__(self, userName, email, pwd, role, type, activated, access_token, id):
    #     self.userName = userName
    #     self.email = email
    #     self.pwd = pwd
    #     self.role = role
    #     self.type = type
    #     self.activated = activated
    #     self.access_token = access_token
    #     self.id = id

    # def to_json(self):
    #     return {
    #         'userName': self.userName,
    #         'email': self.email,
    #         'pwd': self.pwd,
    #         'role': self.role,
    #         'type': self.type,
    #         'activated': self.activated,
    #         'access_token': self.access_token,
    #         'id': self.id,
    #     }


class Archive(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    archiveName = models.CharField(max_length=255)
    dueDate= models.CharField(max_length=255, default='')
    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=255, default='pending')
    progression = models.CharField(max_length=255, default='0%')
    user = models.OneToOneField(EyUser, on_delete=models.PROTECT, default='')  # oneToOne
    equipe = models.OneToOneField(Equipe, on_delete=models.PROTECT, default='')  # oneToOne
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