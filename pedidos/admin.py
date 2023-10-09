from django.contrib import admin

from .models import Pedido, LineaPedido
# Register your models here.

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    readonly_fields=('created_at',)  
    
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ( 'pedido', 'user','cantidad','producto','precio', 'created_at')
    readonly_fields=('created_at',)

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(LineaPedido, LineaPedidoAdmin)



