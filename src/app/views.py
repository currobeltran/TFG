from django.shortcuts import render

def inicio(request):
    return render(request, 'index.html', {})

def buscadorBBDD(request):
    return render(request, 'buscador.html', {})