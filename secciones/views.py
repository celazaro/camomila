from django.shortcuts import render


from tienda.models import Producto
from secciones.models import Secciones
from django.core.paginator import Paginator

from django.db.models import F, ExpressionWrapper, FloatField

# Create your views here.

def secciones(request):
    secciones = Secciones.objects.filter(estado=True)
    
    return render(request,'secciones/secciones.html', {'secciones':secciones} )

def seccion_tipo(request, pk):
    
    secciones = Secciones.objects.all()
    nombre_seccion = Secciones.objects.filter(id = pk)
    productos = Producto.objects.filter(oferta=False, categoria__seccion__id = pk)

    
    # Define el número de elementos por página
    elementos_por_pagina = 8

    # Crea un objeto Paginator
    paginator = Paginator(productos, elementos_por_pagina)

    # Obtiene el número de página a partir de la solicitud GET
    pagina_numero = request.GET.get('page')

    # Obtiene la página actual
    pagina_actual = paginator.get_page(pagina_numero)

    # Código para agregar al QuerySet un elemento nuevo, producto de un cálculo con campos existentes en el modelo

    prod_ofertas = Producto.objects.annotate(
    precio_descuento = ExpressionWrapper(
        F('precio')-F('precio') * F('porcentaje_oferta') / 100,
        output_field=FloatField()
        )
    ) 
    
    prod_ofertas = prod_ofertas.filter(oferta=True, categoria__seccion__id = pk)
    cantidad_prod_ofertas = prod_ofertas.count()
    
    
    context = {
        'secciones':secciones,
        'productos': productos,
        'pagina_actual': pagina_actual,
        'prod_ofertas': prod_ofertas,
        'nombre_seccion': nombre_seccion,
        'cantidad_prod_ofertas': cantidad_prod_ofertas
        
    }
    
    
    return render(request,'secciones/seccion_tipo.html', context)