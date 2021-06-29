# En este documento se almacenarán las vistas de la aplicación web

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ObtenerRegistros
from .forms import *
from .utils import *
import plotly.offline as plotly
import numpy as np
import plotly.graph_objs as go
import csv
from io import StringIO
from django.views.generic import ListView
from django_tables2 import SingleTableView
import random
import datetime
import time

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

        info.remove("Asimilado")
        info.remove("Compartido")
        info.remove("Turno")
        info.remove("GruposReducidos")

        return render(request, 'buscador.html', {'registrado':registrado,'asignaturas':asg,'años':años,'info':info})
    else:
        asg = ObtenerRegistros("Asignatura")
        años = ObtenerAñosUnicos()
        info = ObtenerAtributosTabla("Grupo")

        asgbusqueda = request.POST.getlist('asignaturas[]')
        if not asgbusqueda:
            registros = asg

        añosbusqueda = request.POST.getlist('añoacademico[]')
        if not añosbusqueda:
            añosbusqueda = años
        
        infobusqueda = request.POST.getlist('info[]')
        if not infobusqueda:
            infobusqueda = info
        
        a = ConsultaBusquedaBBDD(asgbusqueda,añosbusqueda,infobusqueda)

        listadatos = []
        listaaños = []
        modoSeleccionado = request.POST.get('customRadio')
        datoAMirar = infobusqueda[infobusqueda.__len__()-1]

        for i in a:
            if modoSeleccionado == 'tabla':
                elemento = {}
                elemento['nombre'] = a[i].get('Nombre')
                elemento['años'] = []
                añosAsignatura = ObtenerAñosAsignatura(a[i].get('PK'))
                grupos = []

                for j in añosbusqueda:
                    año1 = j[0] + j[1] + j[2] + j[3]
                    año2 = j[4] + j[5] + j[6] + j[7]
                    
                    añoelemento = año1 + "/" + año2
                    elemento['años'].append(añoelemento)

                    for añoasig in añosAsignatura:
                        if str(añoasig.Año) == str(j):
                            grupos = ObtenerGruposAño(añoasig.ID)

                # Añadir datos de tabla
                objTabla = []
                for g in grupos:
                    fila = {}
                    if 'Letra' in infobusqueda:
                        fila['Letra'] = g.Letra
                    if 'Nuevos' in infobusqueda:
                        fila['Nuevos'] = g.Nuevos
                    if 'Repetidores' in infobusqueda:
                        fila['Repetidores'] = g.Repetidores
                    if 'Retenidos' in infobusqueda:
                        fila['Retenidos'] = g.Retenidos
                    if 'Plazas' in infobusqueda:
                        fila['Plazas'] = g.Plazas
                    if 'LibreConfiguracion' in infobusqueda:
                        fila['LibreConfiguracion'] = g.LibreConfiguracion
                    if 'OtrosTitulos' in infobusqueda:
                        fila['OtrosTitulos'] = g.OtrosTitulos

                    objTabla.append(fila)
                
                elementoTabla = TablaAsignaturaDatos(objTabla)
                elemento['tabla'] = elementoTabla

                listadatos.append(elemento)

            else:
                # Seleccionar año de búsqueda
                elemento = {}
                elemento['label'] = a[i].get('Nombre')
                añosAsignatura = ObtenerAñosAsignatura(a[i].get('PK'))
                grupos = []
                datosGrafica = []
                cantidad = 0

                for j in añosbusqueda:
                    for añoasig in añosAsignatura:
                        if str(añoasig.Año) == str(j):
                            grupos = ObtenerGruposAño(añoasig.ID)

                    cantidad = 0
                    # Seleccionar grupos de año
                    for g in grupos:
                        if 'Nuevos' in infobusqueda:
                            cantidad += g.Nuevos
                        elif 'Repetidores' in infobusqueda:
                            cantidad += g.Repetidores
                        elif 'Retenidos' in infobusqueda:
                            cantidad += g.Retenidos
                        elif 'Plazas' in infobusqueda:
                            cantidad += g.Plazas
                        elif 'LibreConfiguracion' in infobusqueda:
                            cantidad += g.LibreConfiguracion
                        elif 'OtrosTitulos' in infobusqueda:
                            cantidad += g.OtrosTitulos
                    
                    datosGrafica.append(cantidad)
                
                elemento['data'] = datosGrafica
                valorR = random.randint(0,255)
                valorG = random.randint(0,255)
                valorB = random.randint(0,255)
                elemento['backgroundColor'] = 'rgba('+str(valorR)+','+str(valorG)+','+str(valorB)+', 0.2)'
                listadatos.append(elemento)

        if modoSeleccionado == 'tabla':
            return render(request, "resultadobusqueda.html", {
                'registrado': registrado,   
                'listadatos': listadatos
            })
        else:
            for j in añosbusqueda:
                año1 = j[0] + j[1] + j[2] + j[3]
                año2 = j[4] + j[5] + j[6] + j[7]
                
                añoelemento = año1 + "/" + año2
                listaaños.append(añoelemento)

            return render(request,'grafica.html', {'data': listadatos, 'datoAMirar':datoAMirar, 'listaAños':listaaños, 'registrado':registrado})

def planDocente(request):
    registrado = estaRegistrado(request)
    asignaturas = Asignatura.objects.values()
    
    for i in asignaturas:
        if i['TipoAsignatura'] == 1:
            i['TipoAsignatura'] = "Básica"
        
        añoasig = AñoAsignatura.objects.filter(PK=i['PK']).values()
        i['AL_Anteriores'] = añoasig[0]['Matriculados']
        i['AL_Actuales'] = añoasig[0]['Matriculados']

        gr = ObtenerGruposAño(añoasig[0]['ID'])
        i['GA'] = len(gr)

        numeroGR = 0
        for x in gr:
            numeroGR += x.GruposReducidos

        i['GR'] = numeroGR
        
        if(i['GA'] != 0):
            i['Rat_T'] = '%.3f'%(añoasig[0]['Matriculados']/i['GA'] )
        else:
            i['Rat_T'] = 0
        
        if(i['GR'] != 0):
            i['Rat_P'] = '%.3f'%(añoasig[0]['Matriculados']/i['GR'] )
        else:
            i['Rat_P'] = 0
        
        numeroGR = 0

    tabla = TablaAsignatura(asignaturas)

    return render(request, "plandocente.html", {'registrado': registrado, 'table':tabla})

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
def infomasivaBBDD(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})
    
    if request.method == "GET":
        form = SubirArchivoDatos()
    else:
        form = SubirArchivoDatos(request.POST,request.FILES)
        if form.is_valid():
            content = StringIO(request.FILES['archivo'].read().decode('utf-8'))
            data = csv.DictReader(content)
            for row in data:
                if request.POST['opcion']=="1":
                    if row['IdAsignaturaAnterior'] == "":
                        idanterior=0
                    else:
                        idanterior=int(row['IdAsignaturaAnterior'])

                    if row['PKDif'] == "":
                        pkdif=0
                    else:
                        pkdif=row['PKDif']

                    CrearAsignaturaDesdeCSV(
                        row['Nombre'],
                        pkdif,
                        row['Acronimo'],
                        float(row['CreditosGR']),
                        float(row['CreditosGA']),
                        idanterior,
                        int(row['Curso']),
                        row['Codigo'],
                        int(row['Semestre']),
                        int(row['TipoAsignatura']),
                        int(row['IDMencion'])
                    )
                elif request.POST['opcion']=="2":
                    # 1º paso: Crear un añoasignatura con PK, Curso y matriculados=0 (si no está creado)
                    if not AsignaturaTieneAño(row['PK'], int(row['Curso'])):
                        idañoasig = CrearAñoAsignatura(row['PK'], int(row['Curso']), 0)
                    else:
                        añoasig = ObtenerAñoAsignaturaUnico(row['PK'], int(row['Curso']))
                        idañoasig = añoasig.ID

                    # 2º paso: Crear grupo con información con información restante
                    if row['Asimilado'] == "":
                        asimilado = 0
                    else:
                        asimilado = int(row['Asimilado'])

                    if row['Compartido'] == "":
                        compartido = 0
                    else:
                        compartido = int(row['Compartido'])

                    CrearGrupo(
                        idañoasig=idañoasig,
                        letra=row['LetraGrupo'],
                        nuevos=int(row['Nuevos']),
                        repetidores=int(row['Repetidores']),
                        retenidos=int(row['Retenidos']),
                        plazas=int(row['Plazas']),
                        libreconf=int(row['LibreConfiguracion']),
                        otrostitulos=int(row['OtrosTitulos']),
                        turno=row['Turno'],
                        gruposred=int(row['Subgrupos']),
                        asimilado=asimilado,
                        compartido=compartido
                    )

                    # 3º paso: Recalcular los matriculados de AñoAsignatura
                    nuevosMatriculados = RecalculoDeMatriculados(idañoasig)
                    ModificaMatriculadosAñoAsignatura(idañoasig,nuevosMatriculados)

    return render(request, 'infomasiva.html', {'registrado':registrado,'form':form})

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
                if request.POST.get('PKDif') == "":
                    pkdif = 0
                else:
                    pkdif = request.POST.get('PKDif')

                if request.POST.get('IdAsignaturaAnterior') == "":
                    idanterior = 0
                else:
                    idanterior = request.POST.get('IdAsignaturaAnterior')

                CrearAsignatura(
                    nombre=request.POST.get('Nombre'),
                    pkdif=pkdif,
                    acronimo=request.POST.get('Acronimo'),
                    creditosgr=float(request.POST.get('CreditosGR')),
                    creditosga=float(request.POST.get('CreditosGA')),
                    idasiganterior=idanterior,
                    curso=int(request.POST.get('Curso')),
                    codigo=request.POST.get('Codigo'),
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
                    pkdif=request.POST.get('PKDif'),
                    acronimo=request.POST.get('Acronimo'),
                    creditosgr=float(request.POST.get('CreditosGR')),
                    creditosga=float(request.POST.get('CreditosGA')),
                    idasiganterior=int(request.POST.get('IdAsignaturaAnterior')),
                    curso=int(request.POST.get('Curso')),
                    codigo=request.POST.get('Codigo'),
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
