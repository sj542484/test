from django.db import models
# from django.contrib.auth import models
# Create your models here.
class EquipmentList(models.Model):
    equipment_name = models.CharField(max_length=50)
    equipment_model = models.CharField(max_length=50)
    equipment_uuid = models.CharField(max_length=50,unique=True)
    platform_verion = models.CharField(max_length=50)
    start_but_statue = models.IntegerField(default=0)
    statue_statue = models.IntegerField(default=0)
    gid = models.IntegerField(null=True)
    report = models.CharField(null=True,max_length=100)
    def __str__(self):
        return self.equipment_name

class UserInfo(models.Model):
    username = models.CharField(max_length=50,unique=True)
    pwd = models.CharField(max_length=64)

    def __str__(self):
        return self.username

class SideType(models.Model):
    side = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.side

class ItemType(models.Model):
    side = models.CharField(max_length=50)
    item = models.CharField(max_length=50)

    def __str__(self):
        return self.item