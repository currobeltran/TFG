from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('buscadorBBDD', views.buscadorBBDD, name='buscadorBBDD')
]
