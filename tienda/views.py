from django.shortcuts import render

from tienda.models import Producto
from secciones.models import Secciones
from django.core.paginator import Paginator

from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Round

# Create your views here.

def tienda(request):
    
    secciones = Secciones.objects.all()
    productos = Producto.objects.filter(oferta=False)
    
    
    # Define el número de elementos por página
    elementos_por_pagina = 12

    # Crea un objeto Paginator
    paginator = Paginator(productos, elementos_por_pagina)

    # Obtiene el número de página a partir de la solicitud GET
    pagina_numero = request.GET.get('page')

    # Obtiene la página actual
    pagina_actual = paginator.get_page(pagina_numero)

    # Código para agregar al QuerySet un elemento nuevo, producto de un cálculo con campos existentes en el modelo

    prod_ofertas = Producto.objects.annotate(
    precio_descuento = ExpressionWrapper(
        Round(F('precio')-F('precio') * F('porcentaje_oferta') / 100,2),
        output_field=FloatField()
        )
    ) 
    
    prod_ofertas = prod_ofertas.filter(oferta=True)
    
    
    context = {
        'secciones':secciones,
        'productos': productos,
        'pagina_actual': pagina_actual,
        'prod_ofertas': prod_ofertas,
        
    }
    
    return render(request, 'tienda/tienda.html', context)

