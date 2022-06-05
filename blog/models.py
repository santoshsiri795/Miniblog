from email import message
from unicodedata import name
from django.db import models

# Create your models here.
class post(models.Model):
    title= models.CharField(max_length=250)
    desc = models.TextField()



class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    address=models.CharField(max_length=255)
    message=models.TextField(max_length=500)

    def __str__(self):
        return self.name
        