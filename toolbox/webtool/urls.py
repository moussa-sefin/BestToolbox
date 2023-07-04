from django.urls import  path
from .views import Texteditor,home, tool_details, AddToFavolite, removeFromFavolite, home_for_anonymouse_user,tool_detail_for_anonymous_user       


urlpatterns = [
    path("", home_for_anonymouse_user, name='home_for_anonymouse_user'),
    path("tool-detail/<int:pk>", tool_detail_for_anonymous_user, name='tool_detail_for_anonymous_user'),
    path("home", home, name='home'),
    path('tool_detail/<int:pk>', tool_details, name='tool_detail'),
    path('add-to-favolite/<int:pk>', AddToFavolite.as_view(), name='AddToFavolite'),
    path('remove-from-favolite/<int:pk>', removeFromFavolite, name='removeFromVavolite'),

    path('editor', Texteditor.as_view(), name='Texteditor'),
    
]