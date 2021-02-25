from django.shortcuts import render

def inicio(request):
    return render(request, 'index.html', {'registrado':True})

def buscadorBBDD(request):
    return render(request, 'buscador.html', {'registrado':True})

def editarBBDD(request):
    return render(request, 'editor.html', {'registrado':True})
