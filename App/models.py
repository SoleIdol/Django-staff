from django.db import models


# Create your models here.
class User(models.Model):
    u_name = models.CharField(max_length=32)
    u_password = models.CharField(max_length=256)
    u_age = models.IntegerField(default=22)
    u_gender = models.BooleanField(default=True)
    u_tel = models.CharField(max_length=16)
    u_icon = models.CharField(max_length=128, default='default.jpg')
    
    class Meta:
        db_table = 'user'
