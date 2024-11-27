from rest_framework import serializers
from .models import Publicacion
from django.contrib.auth.models import User

class PublicacionSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Publicacion
        fields = ['id', 'usuario', 'contenido', 'fecha_creacion', 'imagen']

    def create(self, validated_data):
        # Si no se pasa el usuario, se puede asignar un valor predeterminado o dejarlo en blanco
        if 'usuario' not in validated_data:
            validated_data['usuario'] = None  # o asignar un usuario predeterminado
        return Publicacion.objects.create(**validated_data)