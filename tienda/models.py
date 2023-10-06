from django.db import models
from secciones.models import Secciones


# Create your models here.

class CategoriaProd(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    seccion = models.ManyToManyField(Secciones)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    
    class Meta:
        
        verbose_name='CategoriaProductos'
        verbose_name_plural='CategoriasProductos'
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre=models.CharField(max_length=80)
    precio=models.FloatField()
    descripcion=models.CharField(max_length=200)
    informacion=models.TextField() 
    imagen=models.ImageField(default='producto_default.jpeg', upload_to='tienda/') 
    disponibilidad=models.BooleanField(default=True)
    mas_vendido=models.BooleanField(default=False) 
    destacado=models.BooleanField(default=False) 
    oferta=models.BooleanField(default=False)
    porcentaje_oferta=models.IntegerField(default=0)
    categoria=models.ForeignKey(CategoriaProd, on_delete=models.CASCADE) 
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)

    class Meta:
        
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

