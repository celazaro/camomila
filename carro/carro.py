

class Carro:
    
    def __init__(self, request):
        
        if request.user.is_authenticated:  
            self.request=request
            self.session=request.session
            carro=self.session.get("carro")
            if not carro:
                carro=self.session["carro"]={}
        
            self.carro=carro
        
        else:
            self.request=request
            carro=None
            
            if not carro:
                carro={}
        
            self.carro=carro

    def agregar(self,producto):
        if(str(producto.id) not in self.carro.keys()):
            self.carro[producto.id]={
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "precio_unit":str(producto.precio - (producto.precio * producto.porcentaje_oferta / 100)),
                "precio":str(producto.precio - (producto.precio * producto.porcentaje_oferta / 100)),
                "cantidad":1,
                "imagen":producto.imagen.url,

            }
        else:
            for key, value in self.carro.items():
                if key==str(producto.id):
                    value["cantidad"]=value["cantidad"]+1
                    
                    value["precio"] = float(value["precio"]) + (producto.precio - producto.precio * producto.porcentaje_oferta / 100)
                    
                    break
        self.guardar_carro()
        

    def guardar_carro(self):
        self.session["carro"]=self.carro
        self.session.modified=True

    def eliminar(self,producto):
        producto.id=str(producto.id)
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()

    def restar_producto(self, producto):
        for key, value in self.carro.items():
                if key==str(producto.id):
                    precio_reducido = float(value["precio"])-producto.precio
                    value["precio"]=round(precio_reducido, 2)
                    value["cantidad"]=value["cantidad"]-1
                    if value["cantidad"]<1:
                        self.eliminar(producto)
                    break
        self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified=True
        
