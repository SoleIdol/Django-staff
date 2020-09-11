from django.db import models


# Create your models here.
class Employee(models.Model):
    e_name = models.CharField(max_length=32)
    e_gender = models.BooleanField(default=True)
    e_age = models.IntegerField(default=22)
    e_tel = models.CharField(max_length=16)
    e_icon = models.CharField(max_length=128, default='default.jpg')
    
    class Meta:
        db_table = 'employee'
