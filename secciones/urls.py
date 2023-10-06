from django.urls import path
from secciones.views import secciones, seccion_tipo


urlpatterns = [
    
    path('', secciones, name='secciones'),
    path('seccion/<int:pk>', seccion_tipo, name='seccion'),
]