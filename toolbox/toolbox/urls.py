from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static 
from django.urls import ( path,include)
from api import views



from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('contact/', include('contactforms.urls')),

    path("api/", include("api.urls")),
    # path("", include("api.urls")),



 
    
    

]
if settings.DEBUG:     
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)