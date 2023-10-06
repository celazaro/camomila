
from django.urls import path
from core.views import home, blog


urlpatterns = [
    path('', home, name='home'),
    
    path('blog/', blog, name='blog'),
    
]