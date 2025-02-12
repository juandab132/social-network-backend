# Generated by Django 5.1.2 on 2024-11-21 02:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API_GestionUsuariosPerfil', '0007_alter_experiencialaboral_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiencialaboral',
            name='usuario',
        ),
        migrations.AddField(
            model_name='experiencialaboral',
            name='perfil',
            field=models.ForeignKey(default=14, on_delete=django.db.models.deletion.CASCADE, related_name='experiencias', to='API_GestionUsuariosPerfil.perfilusuario'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='experiencialaboral',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='experiencialaboral',
            name='fecha_inicio',
            field=models.DateField(default='2023-01-01'),
            preserve_default=False,
        ),
    ]
