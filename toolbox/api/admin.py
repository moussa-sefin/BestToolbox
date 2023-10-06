from django.contrib import admin

# Register your models here.
# Register your models here.
from . models import (Tool,
                      Tag,
                      Review, 
                      History, 
                      Category, 
                      Favorite,
                      Rating,
                      SharedTool,
                      User,
                      )
                      

admin.site.register([ Tag, Review,Rating, History, Category, Favorite])

@admin.register(Tool)  # Register the Tool model with the admin site
class ToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner', 'license', 'image' )  # Add 'id' to display in the list view
    list_display_links = ('id', 'name','owner')  # Make 'id' and 'name' clickable

@admin.register(SharedTool)  # Register the Tool model with the admin site
class ToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'tool', 'shared_by', )  # Add 'id' to display in the list view
    list_display_links = ('id','tool')  # Make 'id' and 'name' clickable

@admin.register(User)  # Register the Tool model with the admin site
class ToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name','username','email','bio','profile_pic' )  # Add 'id' to display in the list view
    list_display_links = ('id','username')  # Make 'id' and 'name' clickable