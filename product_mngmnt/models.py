from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
 

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    brand= models.CharField(max_length=50 , null=True , blank=True)
    image = models.ImageField(upload_to='media/')
    detail = RichTextField(blank=True , null=True)
    # description =models.TextField(max_length=250)
    def __str__(self):
        return self.name
    
class Visitor(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class UserDetail(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE )
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100,default="")
    mobile_number = models.CharField(max_length=20)
    def __str__(self):
        return self.name