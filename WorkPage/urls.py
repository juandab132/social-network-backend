from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('API_GestionUsuariosPerfil.urls')),
    path('api/publicaciones/', include('API_Publicaciones.urls')), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)