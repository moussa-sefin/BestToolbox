from django.contrib import admin

# Register your models here.
from . models import (Tool,
                      Tag,
                      Rating,
                      Review, 
                      History, 
                      Category, 
                      Favorite)

admin.site.register([Tool, Tag, Rating, Review, History, Category, Favorite])