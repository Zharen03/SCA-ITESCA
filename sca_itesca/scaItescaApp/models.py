from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=255)

class User(models.Model):
    payroll_number = models.PositiveBigIntegerField(primary_key=True, null=False, unique=True)
    password = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.PositiveIntegerField()
    min_gender = models.BooleanField()
    min_general = models.BooleanField()
    role = models.IntegerField()
    status = models.BooleanField()
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    
    