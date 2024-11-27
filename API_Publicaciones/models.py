from django.db import models
from django.contrib.auth.models import User

class Publicacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='publicaciones/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'Publicación de {self.usuario.username} en {self.fecha_creacion}'