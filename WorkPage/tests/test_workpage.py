import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

from API_GestionUsuariosPerfil.models import DatosAcademicos, ExperienciaLaboral, PerfilUsuario
from API_Publicaciones.models import Publicacion

class TestPerfilUsuario(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@test.com'
        )
        
        cls.mi_perfil = PerfilUsuario.objects.create(
            user=user,
            nombre='Juan',
            apellido='Pérez',
            fecha_nacimiento=date(1990, 1, 1)
        )

    def tearDown(self):
        pass

    def test_update_perfil(self):
        url = reverse('editar_perfil', kwargs={'pk': self.mi_perfil.user.id})
        valid_perfil = {
            'nombre': 'Juan Actualizado',
            'apellido': 'Pérez Actualizado',
            'fecha_nacimiento': '1991-01-01'
        }
        valid_perfil_json = json.dumps(valid_perfil)
        response = self.client.put(
            url,
            valid_perfil_json,
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 201])

class TestExperienciaLaboral(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@test.com'
        )
        cls.mi_perfil = PerfilUsuario.objects.create(
            user=user,
            nombre='Juan',
            apellido='Pérez',
            fecha_nacimiento=date(1990, 1, 1)
        )
        
        cls.mi_experiencia = ExperienciaLaboral.objects.create(
            perfil=cls.mi_perfil,
            empresa='Empresa Test',
            puesto='Developer',
            fecha_inicio=date(2020, 1, 1),
            fecha_fin=date(2021, 1, 1),
            descripcion='Descripción test'
        )

class TestPublicacion(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@test.com'
        )
        
        cls.mi_publicacion = Publicacion.objects.create(
            usuario=cls.user,
            contenido='Contenido de prueba'
        )

class TestDatosAcademicos(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@test.com'
        )
        cls.mi_perfil = PerfilUsuario.objects.create(
            user=user,
            nombre='Juan',
            apellido='Pérez',
            fecha_nacimiento=date(1990, 1, 1)
        )
        
        cls.mis_datos = DatosAcademicos.objects.create(
            perfil=cls.mi_perfil,
            institucion='Universidad Test',
            carrera='Ingeniería',
            fecha_inicio=date(2015, 1, 1),
            fecha_fin=date(2020, 1, 1),
            titulo='Ingeniero'
        )