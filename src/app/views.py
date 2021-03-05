from django.shortcuts import render
from django.http import JsonResponse
from .models import ObtenerRegistros
from .forms import *

def inicio(request):
    return render(request, 'index.html', {'registrado':True})

def buscadorBBDD(request):
    return render(request, 'buscador.html', {'registrado':True})

def editarBBDD(request):
    return render(request, 'editor.html', {'registrado':True})

def infomasivaBBDD(request):
    return render(request, 'infomasiva.html', {'registrado':True})

def editaindividual(request):
    return render(request, 'infoindividual.html', {'registrado':True})

def apibuscaBBDD(request):
    x = ObtenerRegistros(request.GET.get('tipo'))
    data = {}
    for i in range(x.__len__()):
        data[i] = x[i]

    return JsonResponse(data)

def copiaSeguridad(request):
    return render(request, 'copiaseguridad.html', {'registrado':True})

def editaUsuario(request):
    return render(request, 'editausuario.html', {'registrado':True})

def formularioEdicion(request):
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
        return render(request, 'error.html', {'registrado':True})

    return render(request, 'formulariogenerado.html', {'registrado':True,'form':form})
