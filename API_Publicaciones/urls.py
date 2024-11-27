from django.urls import path
from .views import (
    CrearPublicacionAPIView, FeedPublicacionesAPIView, ListarPublicacionesAPIView
)

urlpatterns = [
    path('publicaciones/', ListarPublicacionesAPIView.as_view(), name='listar_publicaciones'),
    path('publicaciones/crear/<int:pk>/', CrearPublicacionAPIView.as_view(), name='crear_publicacion'),
    path('feed/<int:user_id>/', FeedPublicacionesAPIView.as_view(), name='feed_publicaciones'),
    
]
