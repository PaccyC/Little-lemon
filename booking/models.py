from django.db import models

# Create your models here.

class Booking(models.Model):
    first_name=models.CharField(max_length=200)
    reservation_date=models.DateTimeField()
    reservation_slot=models.IntegerField()