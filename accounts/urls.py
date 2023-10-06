from django.urls import path
from accounts.views import registrar, PerfilView


urlpatterns = [
    
    path('', registrar, name='registrar'),
    path('perfil', PerfilView.as_view(), name='perfil'),
]