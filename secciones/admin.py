from django.contrib import admin

from .models import Secciones

# Register your models here.

class SeccionesAdmin(admin.ModelAdmin):
    readonly_fields=('fecha_creacion','fecha_modificacion')

admin.site.register(Secciones, SeccionesAdmin)
