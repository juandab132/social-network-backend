from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Publicacion
from .serializers import PublicacionSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser

class CrearPublicacionAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        # Obtener el userId de la URL
        user_id = self.kwargs.get('pk')  # Obtiene el userId de la URL
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Crear una copia mutable de los datos de la solicitud y agregar el usuario
        data = request.data.copy()  # Crear una copia mutable de request.data
        data['usuario'] = usuario.id  # Añadir el ID del usuario a los datos

        # Ahora procedemos a crear la publicación con el nuevo diccionario de datos
        serializer = PublicacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Guardar la publicación
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarPublicacionesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        publicaciones = Publicacion.objects.all().order_by('-fecha_creacion')
        serializer = PublicacionSerializer(publicaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FeedPublicacionesAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        # Obtener las publicaciones de un usuario específico
        publicaciones = Publicacion.objects.all().order_by('-fecha_creacion')

        serializer = PublicacionSerializer(publicaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
