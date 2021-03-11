from django.contrib.postgres.fields import ArrayField
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    price = models.IntegerField()
    image = models.TextField()
    stock = models.CharField(max_length=10, default=100)

    def __str__(self):
        return self.name+" "+str(self.id)


class CustomUser(AbstractUser):
    role = models.CharField(max_length=300)
    def __str__(self):
        return self.username
        
class Contact(models.Model):
    name = models.CharField(max_length=500)
    company_name = models.CharField(max_length=600)
    email  = models.TextField()
    message = models.TextField()
    date = models.DateField()
    
class Order(models.Model):
    name = models.CharField(max_length=500)
    email = models.TextField()
    mobile_number = models.CharField(max_length=10)
    address = models.CharField(max_length=800)
    country = models.CharField(max_length=800)
    state = models.CharField(max_length=800)
    pincode = models.CharField(max_length=500)
    payment_method = models.CharField(max_length=600)
    product_ids = models.CharField(max_length=900,default="NA")
    total_price = models.IntegerField(default=0)
    order_str = models.CharField(max_length=200,default="")
    def __str__(self):
        return self.name
