from argparse import Action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import DatosAcademicos, PerfilUsuario,ExperienciaLaboral
from .serializers import (
    RegistroDatosAcademicosSerializer,
    RegistroDatosSerializer,
    LoginSerializer,
    RegistroExperienciaSerializer,
    RegistroExperienciaSerializer,
    UsuarioSerializer,
    EditarPerfilSerializer,
)

# Vista de registro de usuarios (sin cambios)
class RegistroUsuarioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistroDatosSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "mensaje": "Usuario registrado exitosamente",
                "id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista de inicio de sesión (sin cambios)
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                perfil = user.perfilusuario
                return Response({
                    "mensaje": "Login exitoso",
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "nombre": perfil.nombre,
                    "apellido": perfil.apellido,
                    "fecha_nacimiento": perfil.fecha_nacimiento
                })
            return Response(
                {"error": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para listar todos los usuarios (sin autenticación)
class ListarUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        usuarios = User.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para obtener o editar un perfil de usuario específico
class PerfilUsuarioAPIView(APIView):
    def get(self, request, pk=None):
        try:
            perfil = PerfilUsuario.objects.get(user_id=pk)
            serializer = UsuarioSerializer(perfil.user)
            return Response(serializer.data)
        except PerfilUsuario.DoesNotExist:
            return Response(
                {"error": "Perfil no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk=None):
        try:
            perfil = PerfilUsuario.objects.get(user_id=pk)
            serializer = EditarPerfilSerializer(perfil, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "mensaje": "Información actualizada exitosamente",
                    **serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PerfilUsuario.DoesNotExist:
            return Response(
                {"error": "Perfil no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )


class RegistroExperienciaLaboralAPIView(APIView):
    def post(self, request, id, *args, **kwargs):
        try:
            perfil = PerfilUsuario.objects.get(id=id)
        except PerfilUsuario.DoesNotExist:
            return Response({"error": "Perfil no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Ahora que tenemos el perfil, asociamos la experiencia laboral con él
        experiencia_data = request.data
        experiencia_data['perfil_id'] = perfil.id  # Asociar el perfil al que pertenece la experiencia

        serializer = RegistroExperienciaSerializer(data=experiencia_data)
        if serializer.is_valid():
            experiencia = serializer.save()
            return Response({
                "mensaje": "Experiencia laboral registrada exitosamente",
                "id": experiencia.id,
                "empresa": experiencia.empresa,
                "puesto": experiencia.puesto,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExperienciaLaboralListAPIView(APIView):
    def get(self, request, pk=None):
        try:
            # Obtener las experiencias laborales del perfil del usuario
            experiencias = ExperienciaLaboral.objects.filter(perfil_id=pk)
            serializer = RegistroExperienciaSerializer(experiencias, many=True)
            return Response(serializer.data)
        except ExperienciaLaboral.DoesNotExist:
            return Response(
                {"error": "Experiencia laboral no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )


class RegistroDatosAcademicosAPIView(APIView):
    def post(self, request, id, *args, **kwargs):
        try:
            perfil = PerfilUsuario.objects.get(id=id)
        except PerfilUsuario.DoesNotExist:
            return Response({"error": "Perfil no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Ahora que tenemos el perfil, asociamos 
        academicos_data = request.data
        academicos_data['perfil_id'] = perfil.id  # Asociar el perfil al que pertenece la experiencia

        serializer = RegistroDatosAcademicosSerializer(data=academicos_data)
        if serializer.is_valid():
            academicos = serializer.save()
            return Response({
                "mensaje": "datos academicos registrados exitosamente",
                "id": academicos.id,
                "institucion": academicos.institucion,
                "carrera": academicos.carrera,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DatosAcademicoslListAPIView(APIView):
    def get(self, request, pk=None):
        try:
            # Obtener  del perfil del usuario
            academicos = DatosAcademicos.objects.filter(perfil_id=pk)
            serializer = RegistroDatosAcademicosSerializer(academicos, many=True)
            return Response(serializer.data)
        except DatosAcademicos.DoesNotExist:
            return Response(
                {"error": "datos academicos no encontrados"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        