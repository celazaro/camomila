from django.contrib import admin
from accounts.models import Cliente

# Register your models here.


# PERFIL DETALLADO

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'direccion_calle', 'direccion_otros', 'localidad', 'departamento')

    
# Register your models here.

admin.site.register(Cliente, ClienteAdmin)
