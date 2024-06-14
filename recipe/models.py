from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class fastfood(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.TextField(max_length=100)
    about=models.TextField(max_length=200)
    img=models.ImageField(upload_to="media")


