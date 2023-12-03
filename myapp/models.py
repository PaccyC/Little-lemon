from django.db import models
from datetime import datetime

# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField(default=datetime.now)
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self): 
        return self.first_name



class UserComments(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    comment=models.CharField(max_length=1000)
    

class Menu(models.Model):
   name = models.CharField(max_length=200) 
   price = models.IntegerField(null=False) 
   menu_item_description = models.TextField(max_length=1000, default='') 

   def __str__(self):
      return self.name    