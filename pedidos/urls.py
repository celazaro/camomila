from django.urls import path
from pedidos.views import PedidoView


urlpatterns = [
    
    path('', PedidoView.as_view(), name='completar_pedido'),
    #path('pedido/<int:pk>/', pedido, name='pedido'),
    #path('pago_pedido', pago_pedido, name='pago_pedido')
    
]