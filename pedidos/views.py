
from django.shortcuts import render

from django.views.generic import TemplateView
from accounts.forms import UserForm, ClienteForm
from django.contrib import messages

from pedidos.models import Pedido, LineaPedido
from carro.carro import Carro

from django.db.models import F

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.template.loader import render_to_string
from camomila_web import settings

# Create your views here.

class PedidoView(TemplateView):
    template_name = 'pedidos/pedido.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_form'] = UserForm(instance=user)
        context['cliente_form'] = ClienteForm(instance=user.cliente)

        return super().get_context_data(**kwargs)

    
    def post(self, request, *args, **kwargs):
        
        user = self.request.user
        user_form = UserForm(request.POST, instance=user)
        cliente_form = ClienteForm(request.POST, request.FILES, instance=user.cliente)
        
        contraentrega = request.POST.get('contraentrega')
        tarjeta = request.POST.get('tarjeta')
        transferencia = request.POST.get('transferencia')
                
        cliente_form.fields['direccion_calle'].required = True
        cliente_form.fields['localidad'].required = True
        cliente_form.fields['departamento'].required = True
        cliente_form.fields['codigo_postal'].required = True
        cliente_form.fields['telefono'].required = True

        if  cliente_form.is_valid():
            #user_form.save()    # se deja este formulario comentado ya que no se puede tocar en esta vista
            cliente_form.save()
            
            # Verificar cuántas opciones se han seleccionado
            selected_count = sum(1 for option in [contraentrega, tarjeta, transferencia] if option)

            if selected_count == 1:
                # Solo una opción se seleccionó
                if contraentrega:

                    context = procesar_pedido(request)
                    return render(request, 'pedidos/pago_pedido_contraentrega.html', context) 
                
                elif tarjeta:

                    context = procesar_pedido(request)
                    return render(request, 'pedidos/pago_pedido_tarjeta.html', context)
                
                elif transferencia:

                    context = procesar_pedido(request)
                    return render(request, 'pedidos/pago_pedido_transferencia.html', context)
            else:

                messages.error(request, f'Por favor seleccione una forma de pago.')
                return render(request, 'pedidos/pedido.html')
        
        else:
            for field_name, error_messages in cliente_form.errors.items():
                for error_message in error_messages:
                    messages.error(request, f'Error en {field_name}:  {error_message}')
        
        context = self.get_context_data()
        context['user_form'] = user_form
        context['cliente_form'] = cliente_form

        return render(request, 'pedidos/pedido.html', context)

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

    return resumen_pedido(request, pk=pedido)

def enviar_mail(**kwargs):
    try:
        # Establecemos conexion con el servidor smtp de gmail
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        
        print('conectando...')
        
        pedido = kwargs.get("pedido")
        nombreusuario = kwargs.get("nombreusuario")
        apellidousuario = kwargs.get("apellidousuario")
        email_usuario = kwargs.get("email_usuario")
        total = kwargs.get("total")
        lineapedidos = kwargs.get("lineapedidos")
        
        email_to = email_usuario

        # Construimos el mensaje simple
        mensaje = MIMEMultipart()
        mensaje['From']=settings.EMAIL_HOST
        mensaje['To']=email_to
        mensaje['Subject']="CAMOMILA - Tienda Natural: Confirmación Pedido"
        
        context = {
            'pedido': pedido,
            'nombre' : nombreusuario,
            'apellido' : apellidousuario,
            'lineapedidos' : lineapedidos,
            'total' : total,
        }
        
        content = render_to_string('pedidos/emails/pedido_recibido_correo.html', context)
        mensaje.attach(MIMEText(content, 'html'))
        
        # Envio del mensaje
        mailServer.sendmail(settings.EMAIL_HOST,
                        email_to,
                        mensaje.as_string())
        
        print('Correo enviado con éxito!!!')
        
    except Exception as e:
        print(e)
    

def resumen_pedido(request, pk):
    
    carro = Carro(request)
    
    lineapedidos = LineaPedido.objects.filter(pedido=pk)
    total=0
    total_unidades = 0
    lineapedidos = lineapedidos.annotate(total_producto=F('precio') * F('cantidad'))
    
    for lp in lineapedidos:
        total = total + lp.total_producto
        total_unidades = total_unidades + lp.cantidad
    
    # Insertar el Total del Pedido calculado en la tabla Pedidos, campo importe_total
    obj = pk   # con esto indicamos que el objeto pertenece al pedido en curso
    total_pedido = total
        
    obj.importe_total = total_pedido
    obj.save()
    
    context = {
        'numero_pedido': pk,
        'user': request.user,
        'total': total,
        'total_unidades': total_unidades,
        'lineapedidos': lineapedidos,
    }
    
     # Enviamos mail al cliente
    enviar_mail(
        pedido=pk,
        nombreusuario=request.user.first_name,
        apellidousuario=request.user.last_name,
        email_usuario=request.user.email,
        total=total,
        lineapedidos = lineapedidos,
    )
    
    carro.limpiar_carro()  # agregada por CLA para cerrar sesión carro e iniciar nuevamente
    
    return context
    
def informe_pedidos(request):
    user = request.user
    lineapedido = LineaPedido.objects.filter(user=user)
    pedido = Pedido.objects.filter(user=user)
    
    context = {
         'lineapedido': lineapedido,
         'pedido': pedido,
    }
    
    return render(request,'pedidos/informe_pedidos.html', context)




