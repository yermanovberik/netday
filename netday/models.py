# models.py
from django.db import models


class Registration(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=25)
    country = models.CharField(max_length=100)
    university = models.CharField(max_length=200)
    major = models.CharField(max_length=100)
    course = models.IntegerField()
    isPay = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
