from django.shortcuts import render

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
    return 0
