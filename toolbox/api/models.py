from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    first_name= models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    bio=models.CharField(max_length=255)
    profile_pic=models.ImageField(upload_to='media/images/profile_pic/', null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    
class Tool(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    categories = models.ManyToManyField("Category")
    tags = models.ManyToManyField("Tag")
    download_link = models.URLField(max_length=200, default='https://www.example.com')
    image = models.ImageField(upload_to='media/images/', null=True, blank=True, default="")
    license_choices = [
        ('Open Source', 'Open Source'),
        ('Commercial', 'Commercial'),
    ]
    license = models.CharField(max_length=100, choices=license_choices, )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='tools_owned')
    posted_at = models.DateTimeField(auto_now_add=True, null=True)
   

    def __str__(self):
        return self.name


class Rating(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='ratings', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ratings_given')
    value = models.PositiveSmallIntegerField(default=0)


    def __str__(self):
        return str(self.value)

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tool =  models.ForeignKey(Tool, on_delete=models.CASCADE)

    def __str__(self):
        return self.tool.name
    




class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tool.name

class Review(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='reviews', null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews_given')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.content
    

class SharedTool(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tools_shared_by')
    shared_with = models.ManyToManyField(User, related_name='tools_shared_with')
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tool.name} shared by {self.shared_by.username}"



