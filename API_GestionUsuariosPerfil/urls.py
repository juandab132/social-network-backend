from django.urls import path
from .views import (
    DatosAcademicoslListAPIView,
    ExperienciaLaboralListAPIView, 
    RegistroDatosAcademicosAPIView,
    RegistroExperienciaLaboralAPIView, 
    RegistroUsuarioAPIView, LoginAPIView, PerfilUsuarioAPIView,
    ListarUsuariosAPIView
)

urlpatterns = [
    path('registro/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'),
    path('login/', LoginAPIView.as_view(), name='login_usuario'),
    path('usuarios/', ListarUsuariosAPIView.as_view(), name='listar_usuarios'),
    path('usuarios/<int:pk>/', PerfilUsuarioAPIView.as_view(), name='detalle_usuario'),
    path('experiencia/<int:id>/crear/', RegistroExperienciaLaboralAPIView.as_view(), name='registro_experiencia_laboral'),
    path('usuarios/<int:pk>/experiencia/', ExperienciaLaboralListAPIView.as_view(), name='experiencia_laboral_list'),
    path('academicos/<int:id>/crear/', RegistroDatosAcademicosAPIView.as_view(), name='registro_experiencia_laboral'),
    path('usuarios/<int:pk>/academicos/', DatosAcademicoslListAPIView.as_view(), name='experiencia_laboral_list'),
    path('editar-perfil/<int:pk>/', PerfilUsuarioAPIView.as_view(), name='editar_perfil'),
    
]
