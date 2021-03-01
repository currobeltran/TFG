from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('buscadorBBDD', views.buscadorBBDD, name='buscadorBBDD'),
    path('editorBBDD', views.editarBBDD, name='editorBBDD'),
    path('editormasivo', views.infomasivaBBDD, name='editormasivo'),
    path('editorindividual', views.editaindividual, name='editorindividual'),
    path('api/buscarBBDD', views.apibuscaBBDD, name='buscaBBDD'),
]
