from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ObtenerRegistros
from .forms import *
from .utils import *
import plotly.offline as plotly
import numpy as np
import plotly.graph_objs as go

def inicio(request):
    registrado = estaRegistrado(request)
    return render(request, 'index.html', {'registrado':registrado})

def buscadorBBDD(request):
    registrado = estaRegistrado(request)
    if request.method == "GET":
        asg = ObtenerRegistros("Asignatura")
        años = ObtenerAñosUnicos()
        info = ObtenerAtributosTabla("Grupo")

        return render(request, 'buscador.html', {'registrado':registrado,'asignaturas':asg,'años':años,'info':info})
    else:
        asg = ObtenerRegistros("Asignatura")
        años = ObtenerAñosUnicos()
        info = ObtenerAtributosTabla("Grupo")

        asgbusqueda = request.POST.getlist('asignaturas[]')
        if not asgbusqueda:
            asgbusqueda = ObtenerRegistros("Asignatura")

        añosbusqueda = request.POST.getlist('añoacademico[]')
        if not añosbusqueda:
            añosbusqueda = ObtenerAñosUnicos()
        
        infobusqueda = request.POST.getlist('info[]')
        if not infobusqueda:
            infobusqueda = ObtenerAtributosTabla("Grupo")
        
        a = ConsultaBusquedaBBDD(asgbusqueda,añosbusqueda,infobusqueda)

        curso = go.Figure(
            data=[
                go.Table(
                    header=dict(values=[
                            'Asignatura','Curso', 'AC', 'Cr.GA', 'Cr.GR', 'Cuat', 'Tipo'
                        ]+[atr for x in a for año in a[x].get('Grupos') for atr in a[x].get('Grupos').get(año)]
                    ),
                    cells=dict(values=[
                            [a[x].get('Nombre') for x in a], 
                            [a[x].get('Curso') for x in a], 
                            [a[x].get('Acronimo') for x in a],
                            [a[x].get('Creditos Grupo Amplio') for x in a],
                            [a[x].get('Creditos Grupo Reducido') for x in a],
                            [a[x].get('Semestre') for x in a],
                            [a[x].get('Tipo de Asignatura') for x in a],
                        ]+[a[x].get('Grupos').get(año)[atr] for x in a for año in a[x].get('Grupos') for atr in a[x].get('Grupos').get(año)]
                    )
                )
            ]
        )
        graph = curso.to_html() 

        return render(request, 'resultadobusqueda.html', {'registrado':registrado,'graph':graph})

def editarBBDD(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'editor.html', {'registrado':registrado})

def infomasivaBBDD(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'infomasiva.html', {'registrado':registrado})

def editaindividual(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'infoindividual.html', {'registrado':registrado})

def apibuscaBBDD(request):
    x = ObtenerRegistros(request.GET.get('tipo'))
    data = {}
    for i in range(x.__len__()):
        data[i] = x[i]

    return JsonResponse(data)

def copiaSeguridad(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'copiaseguridad.html', {'registrado':registrado})

def editaUsuario(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    if request.method == 'GET':
        form = EditarUsuarioForm()
        return render(request, 'editausuario.html', {'registrado':registrado, 'usuario':request.user, 'form':form})
    else:
        form = EditarUsuarioForm(request.POST)
        if form.is_valid():
            EditarUsuario(request.user.username, request.POST['nuevo_nombre_de_usuario'], request.POST['nueva_contraseña'])
            return redirect('/accounts/login',request)
        else:
            return render(request, 'editausuario.html', {'registrado':registrado, 'usuario':request.user, 'form':form})

def formularioEdicion(request):
    registrado = estaRegistrado(request)
    form = ''
    nuevo = True

    if request.method == 'POST':
        if request.path == "/formularioedicion/nuevo":
            if request.GET.get('tipo') == "Asignatura":
                CrearAsignatura(
                    nombre=request.POST.get('Nombre'),
                    acronimo=request.POST.get('Acronimo'),
                    creditosgr=int(request.POST.get('CreditosGR')),
                    creditosga=int(request.POST.get('CreditosGA')),
                    idasiganterior=int(request.POST.get('IdAsignaturaAnterior')),
                    curso=int(request.POST.get('Curso')),
                    codigo=int(request.POST.get('Codigo')),
                    semestre=int(request.POST.get('Semestre')),
                    tipoasig=int(request.POST.get('TipoAsignatura')),
                    idmencion=int(request.POST.get('IDMencion'))
                )

            if request.GET.get('tipo') == "Mención":
                CrearMencion(codigo=request.POST.get('Codigo'),nombre=request.POST.get('Nombre'))

            if request.GET.get('tipo') == "Título":
                CrearTitulo(
                    codigo=request.POST.get('Codigo'),
                    nombre=request.POST.get('Nombre'),
                    umbralga=request.POST.get('UmbralGA'),
                    umbralgr=request.POST.get('UmbralGR'),
                    asignaturatitulo=request.POST.getlist('AsignaturaTitulo')
                )
            
            if request.GET.get('tipo') == "Área":
                CrearArea(
                    nombre=request.POST.get('Nombre'),
                    departamento=request.POST.get('Departamento'),
                    acronimo=request.POST.get('Acronimo'),
                    asignaturaarea=request.POST.getlist('AsignaturaArea')
                )
            
            if request.GET.get('tipo') == "Año asignatura":
                CrearAñoAsignatura(
                    pk=request.POST.get('PK'),
                    año=request.POST.get('Año'),
                    matriculados=request.POST.get('Matriculados')
                )

            if request.GET.get('tipo') == "Grupo":
                CrearGrupo(
                    idañoasig=request.POST.get('IDAñoAsignatura'),
                    letra=request.POST.get('Letra'),
                    nuevos=request.POST.get('Nuevos'),
                    repetidores=request.POST.get('Repetidores'),
                    retenidos=request.POST.get('Retenidos'),
                    plazas=request.POST.get('Plazas'),
                    libreconf=request.POST.get('LibreConfiguracion'),
                    otrostitulos=request.POST.get('OtrosTitulos'),
                    turno=request.POST.get('Turno'),
                    gruposred=request.POST.get('GruposReducidos')
                )
        else:
            if request.GET.get('tipo') == "Asignatura":
                idasig = request.GET.get('id')
                ModificaAsignatura(
                    id=idasig,
                    nombre=request.POST.get('Nombre'),
                    acronimo=request.POST.get('Acronimo'),
                    creditosgr=int(request.POST.get('CreditosGR')),
                    creditosga=int(request.POST.get('CreditosGA')),
                    idasiganterior=int(request.POST.get('IdAsignaturaAnterior')),
                    curso=int(request.POST.get('Curso')),
                    codigo=int(request.POST.get('Codigo')),
                    semestre=int(request.POST.get('Semestre')),
                    tipoasig=int(request.POST.get('TipoAsignatura')),
                    idmencion=int(request.POST.get('IDMencion'))
                )
                
            if request.GET.get('tipo') == "Mención":
                idmencion = request.GET.get('id')
                ModificaMencion(id=idmencion,codigo=request.POST.get('Codigo'),nombre=request.POST.get('Nombre'))

        return render(request, 'index.html', {'registrado':registrado})

    if request.GET.get('seleccionobjeto') != "nuevo":
        obj = ObtenerElemento(request.GET.get('selecciontipo'), request.GET.get('seleccionobjeto'))
        nuevo = False

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
        texto = "Lo sentimos, ha ocurrido un error"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'formulariogenerado.html', {'registrado':registrado,'form':form,'nuevo':nuevo,'tipo':request.GET.get('selecciontipo'),
    'objeto':request.GET.get('seleccionobjeto')})
