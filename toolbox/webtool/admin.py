from django.contrib import admin

# Register your models here.
from . models import (Tool,
                      Tag,
                      Review, 
                      History, 
                      Category, 
                      Favorite,
                      Post)

admin.site.register([Post,Tool, Tag, Review, History, Category, Favorite])