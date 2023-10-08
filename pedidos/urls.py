from django.urls import path
from pedidos.views import PedidoView, informe_pedidos


urlpatterns = [
    
    path('', PedidoView.as_view(), name='completar_pedido'),
    path('informe_pedidos', informe_pedidos, name='informe_pedidos')
    
]