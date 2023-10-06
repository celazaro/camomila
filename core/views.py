from django.shortcuts import render
from secciones.models import Secciones
from tienda.models import Producto

# Create your views here.


def home(request):
    
    secciones = Secciones.objects.filter(estado=True)
    prod_destacados = Producto.objects.filter(destacado=True)
    
    return render(request, 'core/home.html', {'secciones':secciones, 'prod_destacados':prod_destacados} )


def blog(request):
    return render(request, 'core/blog.html')


