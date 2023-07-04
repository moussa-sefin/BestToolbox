from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from django_countries.fields import CountryField


class Post(models.Model):
    contents = RichTextField() 
    name = models.CharField(max_length=100)
    country = CountryField()
    images = models.ImageField(null=True)


class Tool(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey("Tag", on_delete=models.SET_NULL, null=True)
    download_link = models.URLField(max_length=200, default='https://www.example.com')
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)
    license = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()

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
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    tool =  models.ForeignKey(Tool, on_delete=models.CASCADE)

    def __str__(self):
        return self.tool.name
    




class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tool.name


class Review(models.Model):
    
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE , default=0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

# class User(models.Model):
#     username = models.CharField(max_length=120)
#     email = models.EmailField()
#     password = models.CharField(max_length=128)
