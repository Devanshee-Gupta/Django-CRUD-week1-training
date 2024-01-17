
from django.db import models
# Create your models here.

class Employee(models.Model):
    Employee_id = models.IntegerField(primary_key = True)
    Employee_name = models.CharField(max_length = 50)


class Departments(models.Model):
    Department_id = models.IntegerField(primary_key = True)
    Department_name = models.CharField(max_length=50)
    Department_manager = models.OneToOneField(Employee, related_name='manager', on_delete=models.CASCADE, null = True) 

