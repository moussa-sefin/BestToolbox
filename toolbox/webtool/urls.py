from django.urls import  path
from .views import home, tool_details           


urlpatterns = [

    path("", home, name='home'),
    path('tool-detail/<int:pk>', tool_details, name='tool_detail'),
]