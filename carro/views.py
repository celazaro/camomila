from django.shortcuts import render

from .carro import Carro

from tienda.models import Producto

from django.shortcuts import redirect

# Create your views here.

def carro(request):
    return render(request,'carro/carro.html')

def agregar_producto(request, producto_id):

    carro=Carro(request)

    producto=Producto.objects.get(id=producto_id)

    carro.agregar(producto=producto)

    return redirect("carro:carro")


def eliminar_producto(request, producto_id):

    carro=Carro(request)

    producto=Producto.objects.get(id=producto_id)

    carro.eliminar(producto=producto)

    return redirect("carro:carro")


def restar_producto(request, producto_id):

    carro=Carro(request)

    producto=Producto.objects.get(id=producto_id)

    carro.restar_producto(producto=producto)

    return redirect("carro:carro")


def limpiar_carro(request):

    carro=Carro(request)

    carro.limpiar_carro()

    return redirect("carro:carro")


