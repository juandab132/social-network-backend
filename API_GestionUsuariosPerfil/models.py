from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, default='ApellidoPorDefecto')
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='experiencias')
    empresa = models.CharField(max_length=255)
    puesto = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f'{self.puesto} en {self.empresa}'



class DatosAcademicos(models.Model):
    perfil = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='academicos', default=1)
    institucion = models.CharField(max_length=255)
    carrera = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.titulo} en {self.institucion} ({self.fecha_inicio} - {self.fecha_fin if self.fecha_fin else "Actual"})'
