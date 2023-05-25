from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tool(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    tag = models.ForeignKey("Tag", on_delete=models.SET_NULL, null=True)
    download_link = models.URLField(max_length=200, default='https://www.example.com')
    image = models.ImageField(upload_to='images/')
    license = models.CharField(max_length=100)


class Rating(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()

class Category(models.Model):
    name = models.CharField(max_length=120)


class Tag(models.Model):
    name = models.CharField(max_length=120)


class Favorite(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    tool =  models.ForeignKey(Tool, on_delete=models.CASCADE)




class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)


class Review(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class User(models.Model):
#     username = models.CharField(max_length=120)
#     email = models.EmailField()
#     password = models.CharField(max_length=128)
