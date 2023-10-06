from django.db import models

# Create your models here.

class Secciones(models.Model):
    titulo = models.CharField(max_length=80)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='secciones/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'
        ordering = ['titulo']
        
    def __str__(self):
        return self.titulo