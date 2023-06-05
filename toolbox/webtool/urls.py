from django.urls import  path
from .views import home, tool_details, AddToFavolite , removeFromFavolite          


urlpatterns = [

    path("", home, name='home'),
    path('tool-detail/<int:pk>', tool_details, name='tool_detail'),
    path('add-to-favolite/<int:pk>', AddToFavolite.as_view(), name='AddToFavolite'),
    path('remove-from-favolite/<int:pk>', removeFromFavolite, name='removeFromVavolite')

]