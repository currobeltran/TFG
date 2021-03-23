# En este documento se almacenarán las vistas de la aplicación web

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ObtenerRegistros
from .forms import *
from .utils import *
import plotly.offline as plotly
import numpy as np
import plotly.graph_objs as go

# Inicio: Vista inicial de la aplicación
# TODO: Añadir un parámetro al renderizado de index.html para que se pueda
# personalizar el mensaje que aparece
def inicio(request):
    registrado = estaRegistrado(request)
    return render(request, 'index.html', {'registrado':registrado})

# BuscadorBBDD: Vista que nos permitirá realizar la operación de búsqueda y
# visualización de información en la base de datos con el objetivo de obtener 
# distintas conclusiones acerca de los datos almacenados.
# 
# La información se podrá mostrar de 2 maneras distintas: en forma de tabla
# y en forma de gráfica, mientras que la información que se pretende mostrar
# será la correspondiente a los grupos de uno o varios años académicos seleccionados
# para una o varias asignaturas concretas. Además, la información de los grupos que 
# se desea visualizar en la tabla o gráfica puede ser cambiada, para ver solo los 
# datos que nos interesen.
# 
# TODO:
#   - Introducir el modo gráfica.
#   - Especificar mejor las características de la visualización de la información que
#     se desea.
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

# EditarBBDD: Vista inicial de la función de edición.
# 
# Dicha función tendrá la capacidad tanto de añadir, eliminar y editar 
# registros presentes en la Base de Datos, pero en esta primera vista
# se mostrará al usuario si desea añadir información de manera masiva
# o de manera individualizada (donde se podrá tanto añadir como editar
# y eliminar).
def editarBBDD(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'editor.html', {'registrado':registrado})

# InfomasivaBBDD: Vista para la introducción de información masiva en la 
# Base de Datos.
# 
# TODO: Dar funcionalidad, solo está diseñada la interfaz.
def infomasivaBBDD(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'infomasiva.html', {'registrado':registrado})

# Editaindividual: Vista para la edición de información individual.
# 
# En esta función se mostrarán 2 menús desplegables con el tipo de dato
# y los objetos del tipo de dato seleccionado respectivamente. Aparecerán 2 
# botones, uno para generar el formulario de edición y otro para la función de 
# eliminación. 
# 
# Dentro del menú desplegable que contendrá los distintos elementos 
# almacenados en la Base de Datos correspondientes a un tipo de dato concreto, siempre
# existirá la opción de crear un elemento nuevo; con el que nos aparecerá un formulario
# en blanco para crear el registro que deseamos. Si en cambio, seleccionasemos un objeto
# ya existente, se generaría el mismo formulario pero relleno con la información del 
# registro seleccionado. Si en vez de editarlo queremos eliminarlo, aparecerá el mismo 
# formulario de manera que no se puedan editar ninguno de los campos que posea.
def editaindividual(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'infoindividual.html', {'registrado':registrado})

# ApibuscaBBDD: Vista para realizar la función de aparición dinámica de 
# los registros de un tipo en concreto.
#
# Básicamente esta función nos ayudará a que, cuando cambiemos de tipo de 
# dato en el menú desplegable de edición de información, se muestren en el
# menú de registros los correspondientes a dicho tipo de dato. En la función se realiza 
# la búsqueda de esta información en la Base de Datos, y el resultado obtenido se envía
# al código JavaScript que ha solicitado esta información a través de una petición AJAX.
def apibuscaBBDD(request):
    x = ObtenerRegistros(request.GET.get('tipo'))
    data = {}
    for i in range(x.__len__()):
        data[i] = x[i]

    return JsonResponse(data)

# CopiaSeguridad: Vista para realizar una copia de seguridad de la información almacenada
# en la Base de Datos.
# TODO: Implementar funcionalidad, solo está diseñada la interfaz.
def copiaSeguridad(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'copiaseguridad.html', {'registrado':registrado})

# EditaUsuario: Vista para que el usuario que esté registrado en ese momento en la aplicación
# pueda editar su infomación personal.
# 
# TODO: Cuando se realiza un cambio efectivo en la información del usuario, se debe dar más
# información a este para que sepa que debe iniciar sesión de nuevo en la aplicación (o implementar
# el inicio de sesión automático tras cambios).
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

# FormularioEdicion: Vista encargada de realizar las acciones cuando se genera un 
# formulario de edición individual en la vista Editaindividual. 
#
# Si la petición que le llega a esta vista es de tipo GET, se genera el formulario
# dependiendo de las características que se hayan introducido anteriormente (se va
# a crear un nuevo elemento->Formulario vacío; se va a editar un elemento ya
# existente->Formulario relleno; se va a eliminar un elemento->Formulario relleno
# no editable).
#
# Si la petición que llega a la función en cambio es de tipo POST, se procesa la información
# que se haya introducido en el formulario para realizar la acción correspondiente (crear,
# editar) y guardarla en la Base de Datos.
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

            if request.GET.get('tipo') == "Título":
                idtitulo = request.GET.get('id')
                ModificaTitulo(
                    id=idtitulo,
                    codigo=request.POST.get('Codigo'),
                    nombre=request.POST.get('Nombre'),
                    umbralga=request.POST.get('UmbralGA'),
                    umbralgr=request.POST.get('UmbralGR'),
                    asignaturatitulo=request.POST.getlist('AsignaturaTitulo')    
                )
            
            if request.GET.get('tipo') == "Área":
                idarea = request.GET.get('id')
                ModificaArea(
                    id = idarea,
                    nombre=request.POST.get('Nombre'),
                    departamento=request.POST.get('Departamento'),
                    acronimo=request.POST.get('Acronimo'),
                    asignaturaarea=request.POST.getlist('AsignaturaArea')
                )
            
            if request.GET.get('tipo') == "Año asignatura":
                idañoasig = request.GET.get('id')
                ModificaAñoAsignatura(
                    id = idañoasig,
                    pk=request.POST.get('PK'),
                    año=request.POST.get('Año'),
                    matriculados=request.POST.get('Matriculados')
                )

            if request.GET.get('tipo') == "Grupo":
                idgrupo = request.GET.get('id')
                ModificaGrupo(
                    id = idgrupo,
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

        return render(request, 'index.html', {'registrado':registrado})

    if request.GET.get('seleccionobjeto') != "nuevo":
        obj = ObtenerElemento(request.GET.get('selecciontipo'), request.GET.get('seleccionobjeto'))
        nuevo = False

    if request.GET.get('selecciontipo') == "Asignatura":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = AsignaturaForm(instance=obj)
            if 'elimina' in request.GET:
                return render(
                    request, 
                    'eliminaregistro.html', 
                    {
                        'registrado':registrado, 
                        'form':form, 
                        'id':request.GET.get('seleccionobjeto'),
                        'tipo':request.GET.get('selecciontipo')
                    }
                )
        else:
            form = AsignaturaForm()

    elif request.GET.get('selecciontipo') == "Área":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = AreaForm(instance=obj)
            if 'elimina' in request.GET:
                return render(
                    request, 
                    'eliminaregistro.html', 
                    {
                        'registrado':registrado, 
                        'form':form, 
                        'id':request.GET.get('seleccionobjeto'),
                        'tipo':request.GET.get('selecciontipo')
                    }
                )
        else:
            form = AreaForm()

    elif request.GET.get('selecciontipo') == "Mención":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = MencionForm(instance=obj)
            if 'elimina' in request.GET:
                return render(
                    request, 
                    'eliminaregistro.html', 
                    {
                        'registrado':registrado, 
                        'form':form, 
                        'id':request.GET.get('seleccionobjeto'),
                        'tipo':request.GET.get('selecciontipo')
                    }
                )
        else:
            form = MencionForm()

    elif request.GET.get('selecciontipo') == "Título":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = TituloForm(instance=obj)
            if 'elimina' in request.GET:
                return render(
                    request, 
                    'eliminaregistro.html', 
                    {
                        'registrado':registrado, 
                        'form':form, 
                        'id':request.GET.get('seleccionobjeto'),
                        'tipo':request.GET.get('selecciontipo')
                    }
                )
        else:
            form = TituloForm()

    elif request.GET.get('selecciontipo') == "Año asignatura":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = AñoAsignaturaForm(instance=obj)
            if 'elimina' in request.GET:
                return render(
                    request, 
                    'eliminaregistro.html', 
                    {
                        'registrado':registrado, 
                        'form':form, 
                        'id':request.GET.get('seleccionobjeto'),
                        'tipo':request.GET.get('selecciontipo')
                    }
                )
        else:
            form = AñoAsignaturaForm()

    elif request.GET.get('selecciontipo') == "Grupo":
        if request.GET.get('seleccionobjeto') != "nuevo":
            form = GrupoForm(instance=obj)
            if 'elimina' in request.GET:
                return render(
                    request, 
                    'eliminaregistro.html', 
                    {
                        'registrado':registrado, 
                        'form':form, 
                        'id':request.GET.get('seleccionobjeto'),
                        'tipo':request.GET.get('selecciontipo')
                    }
                )
        else:
            form = GrupoForm()

    if form == '':
        texto = "Lo sentimos, ha ocurrido un error"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    return render(request, 'formulariogenerado.html', {'registrado':registrado,'form':form,'nuevo':nuevo,'tipo':request.GET.get('selecciontipo'),
    'objeto':request.GET.get('seleccionobjeto')})

# EliminaRegistro: Vista para realizar la eliminación de un registro almacenado
# en la Base de Datos.
def eliminaRegistro(request):
    registrado = estaRegistrado(request)
    # Obtener elemento a eliminar a traves de id (desde url) y mandar peticion de eliminado a BBDD
    EliminaObjeto(request.GET.get('id'),request.GET.get('tipo'))

    return render(request, 'index.html', {'registrado':registrado})
