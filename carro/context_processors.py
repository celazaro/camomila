def importe_total_carro(request):
    total=0
    
    if 'carro' not in request.session:
        return {"importe_total_carro": total}
    
    for key,value in request.session["carro"].items():
        
        precio=float(value["precio"])
        total = total + precio
       
    return {"importe_total_carro":total}


def articulos_total_carro(request):
    articulos=0
    
    if 'carro' not in request.session:
        return {'articulos_total_carro': articulos}
    
    for key,value in request.session['carro'].items():
        articulos=articulos+value['cantidad']

    return {'articulos_total_carro':articulos}

