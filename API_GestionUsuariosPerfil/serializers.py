from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User


from .models import DatosAcademicos, ExperienciaLaboral, PerfilUsuario

class RegistroDatosSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    fecha_nacimiento = serializers.DateField()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'nombre', 'apellido', 'fecha_nacimiento']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        nombre = validated_data.pop('nombre')
        apellido = validated_data.pop('apellido')
        fecha_nacimiento = validated_data.pop('fecha_nacimiento')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        PerfilUsuario.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento
        )

        return user
    

class RegistroExperienciaSerializer(serializers.ModelSerializer):
    perfil_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ExperienciaLaboral
        fields = ['perfil_id', 'empresa', 'puesto', 'fecha_inicio', 'fecha_fin', 'descripcion']

    def create(self, validated_data):
        perfil_id = validated_data.pop('perfil_id')
        try:
            perfil = PerfilUsuario.objects.get(id=perfil_id)
        except PerfilUsuario.DoesNotExist:
            raise serializers.ValidationError("Perfil no encontrado.")

        experiencia = ExperienciaLaboral.objects.create(perfil=perfil, **validated_data)
        return experiencia

class RegistroDatosAcademicosSerializer(serializers.ModelSerializer):
    perfil_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = DatosAcademicos
        fields = ['perfil_id', 'institucion', 'carrera', 'fecha_inicio', 'fecha_fin', 'titulo']

    def create(self, validated_data):
        perfil_id = validated_data.pop('perfil_id')
        try:
            perfil = PerfilUsuario.objects.get(id=perfil_id)
        except PerfilUsuario.DoesNotExist:
            raise serializers.ValidationError("Perfil no encontrado.")

        datos_academicos = DatosAcademicos.objects.create(perfil=perfil, **validated_data)
        return datos_academicos

    
class UsuarioSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='perfilusuario.nombre')
    apellido = serializers.CharField(source='perfilusuario.apellido')
    fecha_nacimiento = serializers.DateField(source='perfilusuario.fecha_nacimiento')
    experiencias = RegistroExperienciaSerializer(source='perfilusuario.experiencias', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nombre', 'apellido', 'fecha_nacimiento', 'experiencias']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class EditarPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['nombre', 'apellido', 'fecha_nacimiento']

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value

    def validate_apellido(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido no puede estar vacío")
        return value

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.apellido = validated_data.get('apellido', instance.apellido)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.save()
        return instance
    

