from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from pedidos.models import Pedido, LineaPedido
from carro.carro import Carro
from pedidos.models import LineaPedido
from django.db.models import F
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.utils.html import strip_tags


from django.contrib import messages

# Create your views here.

def pedido(request, pk):
    
    carro = Carro(request)
    
    lineapedidos = LineaPedido.objects.filter(pedido=pk)
    total=0
    total_unidades = 0
    lineapedidos = lineapedidos.annotate(total_producto=F('precio') * F('cantidad'))
    
    for lp in lineapedidos:
        total = total + lp.total_producto
        total_unidades = total_unidades + lp.cantidad
    
    
    context = {
        'numero_pedido': pk,
        'user': request.user,
        
        'total': total,
        'total_unidades': total_unidades,
        'lineapedidos': lineapedidos,
    }
    
    #carro.limpiar_carro()  # agregada por CLA para cerrar sesión carro e iniciar nuevamente
    
    return render(request, 'pedidos/pedido.html', context)




@login_required(login_url='/accounts/login')

def procesar_pedido(request):
    pedido=Pedido.objects.create(user=request.user) # damos de alta un pedido
    carro=Carro(request)  # cogemos el carro
    lineas_pedido=list()  # lista con los pedidos para recorrer los elementos del carro
    for key, value in carro.carro.items(): #recorremos el carro con sus items
        lineas_pedido.append(LineaPedido(
            producto_id=key,
            cantidad=value['cantidad'],
            user=request.user,
            pedido=pedido,
            precio=value['precio_unit'],
            
                            
            ))

    LineaPedido.objects.bulk_create(lineas_pedido) # crea registros en BBDD en paquete
    #enviamos mail al cliente
    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        nombreusuario=request.user.username,
        email_usuario=request.user.email
        

    )
    #mensaje para el futuro
    #messages.success(request, "El pedido se ha creado correctamente")
    
    
    
    return redirect('pedido', pk=pedido)  

def enviar_mail(**kwargs):
    asunto="CAMOMILA - Tienda Natural :  Confirmación de Pedido"
    mensaje=render_to_string("pedidos/emails/email_pedido.html", {
        "pedido": kwargs.get("pedido"),
        "lineas_pedido": kwargs.get("lineas_pedido"),
        "nombreusuario":kwargs.get("nombreusuario"),
        "email_usuario":kwargs.get("email_usuario"),
        })

    mensaje_texto=strip_tags(mensaje)
    from_email="c4rl0s.l4z4r0@gmail.com"
    to=kwargs.get("email_usuario")
    
    send_mail(asunto,mensaje_texto,from_email,[to], html_message=mensaje)
    
