from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import os

from django.conf import settings
from django.core.files.storage import default_storage

# Ahora, modifica las propiedades de los campos first_name y last_name en el modelo User
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False


# Create your models here.


class Cliente(models.Model):
    user=models.OneToOneField( User, on_delete=models.CASCADE, related_name='cliente', verbose_name='Usuario' )
    imagen = models.ImageField( default='perfil_default.png', upload_to='users/' )
    direccion_calle=models.CharField(max_length=100, null=False, blank=True)
    direccion_otros=models.CharField(max_length=200, null=False, blank=True)
    localidad=models.CharField(max_length=100, null=False, blank=True)
    departamento=models.CharField(max_length=100, null=False, blank=True)
    codigo_postal=models.CharField(max_length=10, null=False, blank=True)
    telefono=models.CharField(max_length=20, null=False, blank=True)
    direccion_alternativa=models.CharField(max_length=200, null=False, blank=True)
    notas=models.TextField(null=False, blank=True)
    
    def save(self, *args, **kwargs):
    # Verificar que la imagen que estoy subiendo es diferente a la predeterminada
        if self.pk and self.imagen.name != 'perfil_default.png':
            viejo_perfil = Cliente.objects.get(pk=self.pk)
            default_imagen_path = os.path.join(settings.MEDIA_ROOT, 'perfil_default.png')
            
            if viejo_perfil.imagen.path != self.imagen.path and viejo_perfil.imagen.path != default_imagen_path:
                # Voy a eliminar la imagen anteniro si es distinta de la actual y distinta de perfil_default.png
                default_storage.delete(viejo_perfil.imagen.path)
            
        super(Cliente, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table='cliente'
        verbose_name='Cliente'
        verbose_name_plural='Clientes'
        ordering=['-id']



def create_user_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)

def save_user_cliente(sender, instance, **kwargs):
    instance.cliente.save()

post_save.connect(create_user_cliente, sender=User)
post_save.connect(save_user_cliente, sender=User)