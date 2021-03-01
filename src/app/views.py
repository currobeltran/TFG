from django.shortcuts import render
from django.http import JsonResponse
from .models import ObtenerRegistros

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
    data = { i:i for i in x }
    return JsonResponse(data)
