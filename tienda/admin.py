from django.contrib import admin
from tienda.models import CategoriaProd, Producto


# Register your models here.

class CategoriaProdAdmin(admin.ModelAdmin):
    readonly_fields=('fecha_creacion','fecha_modificacion')
    
    
admin.site.register(CategoriaProd, CategoriaProdAdmin)

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields=('fecha_creacion','fecha_modificacion')
    list_display =('nombre', 'precio', 'disponibilidad', 'mas_vendido', 'destacado', 'oferta','porcentaje_oferta', 'categoria', 'estado')
    
admin.site.register(Producto, ProductoAdmin)


