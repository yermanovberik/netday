from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Registration(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    surname = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    email = models.EmailField(
        unique=True,
        null=False
    )
    phone_number = models.CharField(
        max_length=25,
        null=False,
        blank=False
    )
    country = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    university = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    major = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    course = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='Value should be at least 1'),
            MaxValueValidator(9, message='Value should be at most 9')
        ],
        null=False
    )
    isPay = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
