from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Post model.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) #Author
    title = models.CharField(max_length=150) #Title
    image = models.ImageField(null = True,blank=True) #Image
    description = models.TextField() #Desciption
    created_at = models.DateTimeField(auto_now_add=True) #Creation
    updated_at = models.DateTimeField(auto_now=True) #Update

    def __str__(self):
        return self.title + "\n" + self.description + "\n" + str(self.image)
    
