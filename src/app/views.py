from django.shortcuts import render
from django.http import JsonResponse
from .models import ObtenerRegistros
from .forms import *
from .utils import *

def inicio(request):
    registrado = estaRegistrado(request)
    return render(request, 'index.html', {'registrado':registrado})

def buscadorBBDD(request):
    registrado = estaRegistrado(request)
    return render(request, 'buscador.html', {'registrado':registrado})

def editarBBDD(request):
    registrado = estaRegistrado(request)
    return render(request, 'editor.html', {'registrado':registrado})

def infomasivaBBDD(request):
    registrado = estaRegistrado(request)
    return render(request, 'infomasiva.html', {'registrado':registrado})

def editaindividual(request):
    registrado = estaRegistrado(request)
    return render(request, 'infoindividual.html', {'registrado':registrado})

def apibuscaBBDD(request):
    x = ObtenerRegistros(request.GET.get('tipo'))
    data = {}
    for i in range(x.__len__()):
        data[i] = x[i]

    return JsonResponse(data)

def copiaSeguridad(request):
    registrado = estaRegistrado(request)
    return render(request, 'copiaseguridad.html', {'registrado':registrado})

def editaUsuario(request):
    registrado = estaRegistrado(request)
    return render(request, 'editausuario.html', {'registrado':registrado})

def formularioEdicion(request):
    registrado = estaRegistrado(request)
    form = ''

    if request.GET.get('seleccionobjeto') != "nuevo":
        obj = ObtenerElemento(request.GET.get('selecciontipo'), request.GET.get('seleccionobjeto'))

    if request.GET.get('selecciontipo') == "Asignatura":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = AsignaturaForm(instance=obj)
        else:
            form = AsignaturaForm()

    elif request.GET.get('selecciontipo') == "Área":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = AreaForm(instance=obj)
        else:
            form = AreaForm()

    elif request.GET.get('selecciontipo') == "Mención":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = MencionForm(instance=obj)
        else:
            form = MencionForm()

    elif request.GET.get('selecciontipo') == "Título":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = TituloForm(instance=obj)
        else:
            form = TituloForm()

    elif request.GET.get('selecciontipo') == "Año asignatura":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = AñoAsignaturaForm(instance=obj)
        else:
            form = AñoAsignaturaForm()

    elif request.GET.get('selecciontipo') == "Grupo":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = GrupoForm(instance=obj)
        else:
            form = GrupoForm()

    if form == '':
        return render(request, 'error.html', {'registrado':registrado})

    return render(request, 'formulariogenerado.html', {'registrado':registrado,'form':form})
