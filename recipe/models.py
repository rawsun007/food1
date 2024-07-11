from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class fastfood(models.Model):
    name=models.TextField(max_length=100)
    about=models.TextField(max_length=200)
    img=models.ImageField(upload_to="media")
   

class SavedRecipe(models.Model):
    recipe_label = models.CharField(max_length=500)
    recipe_url = models.URLField(max_length=2000)
    recipe_image = models.URLField(max_length=2000, null=True, blank=True)
    meal_type = models.CharField(max_length=1000, null=True, blank=True) 
    cuisine_type = models.CharField(max_length=1000, null=True, blank=True)  
    source = models.CharField(max_length=1000, null=True, blank=True)  

    def __str__(self):
        return self.recipe_label




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_recipes_savedrecipe = models.ManyToManyField(SavedRecipe, related_name='saved_by')

    def __str__(self):
        return self.user.username