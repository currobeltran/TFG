# En este documento se almacenarán las vistas de la aplicación web

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ObtenerRegistros
from .forms import *
from .utils import *
import numpy as np
from sklearn.linear_model import LinearRegression
import csv
from io import StringIO
from django.views.generic import ListView
from django_tables2 import SingleTableView
import random
import datetime
import time
from django.core.management import call_command
import os
from django.apps import apps

# Inicio: Vista inicial de la aplicación
def inicio(request):
    registrado = estaRegistrado(request)
    return render(request, 'index.html', {'registrado':registrado, 'msg':"Bienvenido a la aplicación"})

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
def buscadorBBDD(request):
    registrado = estaRegistrado(request)
    if request.method == "GET":
        asg = ObtenerRegistros("Asignatura")
        años = ObtenerAñosUnicos()
        info = ObtenerAtributosTabla("Grupo")

        info.remove("Asimilado")
        info.remove("Compartido")
        info.remove("Turno")

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

        for i in a:
            if modoSeleccionado == 'tabla':
                añosAsignatura = ObtenerAñosAsignatura(a[i].get('PK'))

                for j in añosbusqueda:
                    añoelemento = formatearAnio(j)

                    for añoasig in añosAsignatura:
                        if str(añoasig.Año) == str(j):
                            elemento = {}
                            elemento['nombre'] = a[i].get('Nombre')
                            elemento['año'] = añoelemento
                            elemento['id'] = a[i].get('PK')+j

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
                                    fila['Libre Configuracion'] = g.LibreConfiguracion
                                if 'OtrosTitulos' in infobusqueda:
                                    fila['Otros Titulos'] = g.OtrosTitulos
                                if 'GruposReducidos' in infobusqueda:
                                    fila['Grupos Reducidos'] = g.GruposReducidos

                                objTabla.append(fila)
                            
                            elemento['tabla'] = objTabla

                            listadatos.append(elemento)

            else:
                # Ordenamos la información de manera que cada
                # línea de la gráfica se corresponda con un valor
                # concreto de los seleccionados para una asignatura concreta
                #
                # Para todos los valores que se desean consultar:
                for elementoABuscar in infobusqueda:
                    elemento = {}
                    
                    # Establecemos como etiqueta el nombre de la asignatura y el parámetro consultado
                    elemento['label'] = "Alumnos " + elementoABuscar + " en " + a[i].get('Nombre')

                    # Obtenemos todos los objetos añoAsignaturas asociados a esta asignatura
                    añosAsignatura = ObtenerAñosAsignatura(a[i].get('PK'))

                    # Declaramos variables vacias que se rellenarán en el siguiente bucle
                    grupos = []
                    datosGrafica = []
                    cantidad = 0

                    # Para cada año seleccionado en el formulario:
                    for j in añosbusqueda:
                        # Para todos los años de la asignatura actual:
                        for añoasig in añosAsignatura:
                            # Si el año de busqueda actual (j) 
                            # es igual al año de la asignatura actual (añoasig) 
                            # obtenemos los grupos de dicho año para dicha asignatura
                            if str(añoasig.Año) == str(j):
                                grupos = ObtenerGruposAño(añoasig.ID)

                        cantidad = 0
                        # Para todos los grupos:
                        for g in grupos:
                            # Si el parámetro de búsqueda es igual a uno de los siguientes:
                                # se suma el valor del parámetro dentro del grupo actual a la variable cantidad
                            if 'Nuevos' == elementoABuscar:
                                cantidad += g.Nuevos
                            elif 'Repetidores' == elementoABuscar:
                                cantidad += g.Repetidores
                            elif 'Retenidos' == elementoABuscar:
                                cantidad += g.Retenidos
                            elif 'Plazas' == elementoABuscar:
                                cantidad += g.Plazas
                            elif 'LibreConfiguracion' == elementoABuscar:
                                cantidad += g.LibreConfiguracion
                            elif 'OtrosTitulos' == elementoABuscar:
                                cantidad += g.OtrosTitulos
                        
                        # cantidad tiene como valor el número de alumnos totales 
                        # de un parámetro determinado en un único año académico de 
                        # de una asignatura concreta
                        datosGrafica.append(cantidad)
                    
                    # datosGrafica contiene la serie de valores de un parámetro determinado
                    # para una asignatura concreta durante los años seleccionados
                    elemento['data'] = datosGrafica

                    # Se configuran los colores de las líneas que tendrán estas series de 
                    # valores dentro de la gráfica
                    valorR = random.randint(0,255)
                    valorG = random.randint(0,255)
                    valorB = random.randint(0,255)
                    elemento['borderColor'] = 'rgba('+str(valorR)+','+str(valorG)+','+str(valorB)+', 1)'
                    elemento['backgroundColor'] = 'rgba(255,255,255,0)'

                    # Se incorpora el elemento con toda la información recogida anteriormente
                    # a la lista que tendrá todos los datos correspondientes a la gráfica que
                    # se va a crear
                    listadatos.append(elemento)

        if modoSeleccionado == 'tabla':
            return render(request, "resultadobusqueda.html", {
                'registrado': registrado,   
                'listadatos': listadatos
            })
        else:
            # Se genera una lista de años que se colocará en el eje x de la gráfica
            # Dicha lista será formateada y ordenada para que el año más antiguo aparezca
            # más cercano al eje y
            for j in añosbusqueda:
                añoelemento = formatearAnio(j)
                listaaños.append(añoelemento)
            
            listaaños.sort()
            return render(request,'grafica.html', {'data': listadatos, 'listaAños':listaaños, 'registrado':registrado})

# planDocente: Vista que genera las tablas correspondientes
# a un plan de ordenación docente
def planDocente(request):
    registrado = estaRegistrado(request)

    # Obtenemos todas las asignaturas
    asignaturas = Asignatura.objects.values()
    
    # Creamos un diccionario que rellenaremos con las distintas tablas del plan docente
    tablas = {}
    
    # Si no hay más de 3 años académicos dentro de la aplicación, no se genera el plan docente
    añosUnicos = ObtenerAñosUnicos()
    if añosUnicos.__len__()<3 :
        return render(request, 'index.html', {'registrado':registrado, 'msg':"Error: No existen datos suficientes para generar el plan docente"})
    
    # Vector de los 3 últimos años académicos almacenados
    cursos = [añosUnicos[2],añosUnicos[1],añosUnicos[0]]

    # Para cada asignatura:
    for i in asignaturas:
        # El diccionario elemento corresponderá con una fila de una tabla del plan docente
        elemento = {}

        # Se rellenan las distintas columnas con la información general de la asignatura
        elemento['Nombre'] = i.get('Nombre')
        elemento['Acronimo'] = i.get('Acronimo')
        elemento['CRGA'] = i.get('CreditosGA')
        elemento['CRGR'] = i.get('CreditosGR')
        elemento['Cuatrimestre'] = i.get('Semestre')
        elemento['Tipo'] = i.get('TipoAsignatura')

        # Se modifica el campo 'Tipo' por un string, correspondiente al nombre del tipo 
        # de la asignatura dentro de la titulación a la que pertenece
        elemento = defineTipoAsignaturaPlanDocenteInformatica(elemento,i)
 
        # Obtenemos los objetos AñoAsignatura correspondientes a los 3 últimos cursos académicos
        añoAsignatura1 = ObtenerAñoAsignaturaUnico(i.get('PK'), cursos[0]) # Año más reciente
        añoAsignatura2 = ObtenerAñoAsignaturaUnico(i.get('PK'), cursos[1])
        añoAsignatura3 = ObtenerAñoAsignaturaUnico(i.get('PK'), cursos[2]) # Año más antiguo

        # Se rellenan columnas con información obtenida de los objetos AñoAsignatura anteriores
        elemento['AlumnosAnteriorespasado'] = añoAsignatura3.Matriculados
        elemento['AlumnosActualespasado'] = añoAsignatura2.Matriculados
        elemento['AlumnosAnterioresactual'] = añoAsignatura2.Matriculados
        elemento['AlumnosActualesactual'] = añoAsignatura1.Matriculados

        # Obtenemos los grupos de los 2 años más recientes
        grupos1 = ObtenerGruposAño(añoAsignatura2.ID)
        grupos2 = ObtenerGruposAño(añoAsignatura1.ID)

        # Se rellenan columnas con información obtenida de los objetos Grupo anteriores
        elemento['GruposGrandespasado'] = grupos1.__len__()
        elemento['GruposGrandesactual'] = grupos2.__len__()
        elemento['GruposReducidospasado'] = 0
        elemento['GruposReducidosactual'] = 0

        # Cálculo del número de grupos reducidos en los 2 años más recientes 
        # 
        # Se obtiene este número a partir de acumular la cantidad de grupos reducidos de
        # todos los grupos de la asignatura en dicho año 
        elemento['GruposReducidospasado'] = numeroGruposReducidosEnAño(grupos1)
        elemento['GruposReducidosactual'] = numeroGruposReducidosEnAño(grupos2)

        # Se obtienen las ratios de alumnos por grupo en teoría y prácticas.
        # 
        # Si no existen grupos reducidos para esa asignatura, antes que realizar una división
        # entre 0 se comprueba para evitar el error
        elemento['RatioTeoriapasado'] = round(añoAsignatura2.Matriculados/grupos1.__len__(),2)
        if elemento['GruposReducidospasado'] != 0:
            elemento['RatioPracticaspasado'] = round(añoAsignatura2.Matriculados/elemento['GruposReducidospasado'],2)
        else:
            elemento['RatioPracticaspasado'] = 0

        elemento['RatioTeoriaactual'] = round(añoAsignatura1.Matriculados/grupos2.__len__(),2)
        if elemento['GruposReducidosactual'] != 0:
            elemento['RatioPracticasactual'] = round(añoAsignatura1.Matriculados/elemento['GruposReducidosactual'],2)
        else:
            elemento['RatioPracticasactual'] = 0

        # Diferencia de alumnos matriculados
        elemento['Diferencia'] = añoAsignatura1.Matriculados - añoAsignatura2.Matriculados

        # Incremento de los créditos utilizados en teoría entre el penúltimo año y el último registrados
        elemento['IncrementoTeoria'] = (grupos2.__len__()-grupos1.__len__())*i.get('CreditosGA')

        # Incremento de los créditos utilizados en prácticas entre el penúltimo año y el último registrados
        elemento['IncrementoPractica'] = (elemento['GruposReducidosactual']-elemento['GruposReducidospasado'])*i.get('CreditosGR')

        # Suma de los incrementos totales de créditos en teoría y prácticas
        elemento['IncrementoTotal'] = elemento['IncrementoTeoria']+elemento['IncrementoPractica']

        # Cantidad total de créditos utilzados para el último curso registrado
        elemento['Creditos'] = (grupos2.__len__()*i.get('CreditosGA'))+(elemento['GruposReducidosactual']*i.get('CreditosGR'))

        # Se añade el elemento a la lista correspondiente a su curso
        tablas = aniadeAsignaturaInformaticaAPlanDocente(tablas,i,elemento)

    return render(
        request,
        "plandocente.html",
        {
            'registrado': registrado, 
            'tablas': tablas,
            'numerotablas': tablas.__len__()
        }
    )

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

def apiBuscaAsignaturasPorSemestre(request):
    x = ObtenerAsignaturasPorSemestre(request.GET.get('semestre'))
    data = {}

    for i in range(x.__len__()):
        data[i] = {'PK': x[i].PK,'Nombre': x[i].Nombre}

    return JsonResponse(data)

# CopiaSeguridad: Vista para realizar y restaurar 
# una copia de seguridad de la información almacenada en la Base de Datos.
def copiaSeguridad(request):
    registrado = estaRegistrado(request)
    if not registrado:
        texto = "No tiene permiso para acceder a esta página"
        return render(request, 'error.html', {'registrado':registrado, 'texto':texto})

    if request.method == "GET":
        return render(request, 'copiaseguridad.html', {'registrado':registrado})

    else:

        if request.POST.get('accion') == '1':
            backup = open(os.path.dirname(apps.get_app_config("app").path)+"/var/backups/"+request.POST.get('nombreDocumento')+".json",'w')
            call_command('dumpdata',stdout=backup)
            backup.close()
            
            return render(request, 'index.html', {'registrado':registrado,'msg':"Copia de seguridad realizada"})

        elif request.POST.get('accion') == '2':
            if request.POST.get('archivo') == '':
                return render(request, 'copiaseguridad.html', {'registrado':registrado})

            call_command('loaddata',os.path.dirname(apps.get_app_config("app").path)+"/var/backups/"+request.POST.get('archivo'))

            return render(request, 'index.html', {'registrado':registrado,'msg':"Copia de seguridad reestablecida"})
        
        return render(request, 'index.html', {'registrado':registrado,'msg':"Lo sentimos, ha ocurrido un error"})

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

        return render(request, 'index.html', {'registrado':registrado, 'msg':"Operación realizada correctamente"})

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

    return render(request, 'index.html', {'registrado':registrado, 'msg':"Registro eliminado correctamente"})

# Predicciones: Vista desde la cual se realizarán las predicciones que será capaz de 
# producir la aplicación.
def predicciones(request):
    registrado = estaRegistrado(request)

    if request.method == "GET":
        return render(request, 'predicciones.html', {'registrado':registrado})
    
    else:
        # Obtención de asignatura seleccionada y lista de años
        pkAsignaturas = request.POST.getlist('asignaturas[]')
        vectorAsignaturas = []
        for i in pkAsignaturas:
            vectorAsignaturas.append(ObtenerElemento('Asignatura',i))
        
        añosUnicos = ObtenerAñosUnicos()
        añoActual = añosUnicos[añosUnicos.__len__()-1]
        añoActual = str(añoActual)
        añoActual = formatearAnio(añoActual)

        añoProximo = añosUnicos[añosUnicos.__len__()-1] + 10001
        añoProximo = str(añoProximo)
        añoProximo = formatearAnio(añoProximo)

        añoProximo2 = añosUnicos[añosUnicos.__len__()-1] + 20002
        añoProximo2 = str(añoProximo2)
        añoProximo2 = formatearAnio(añoProximo2)

        infoGrafica = []
        tablasActual = []
        tablasPrediccion = []
        arrayPrecision = []
        nombresAsignaturas = []
        # Obtención de datos y regresión lineal
        for asg in vectorAsignaturas:
            nombresAsignaturas.append(asg.Nombre)
            print(asg.Nombre)

            añosAsignatura = ObtenerAñosAsignatura(asg.PK)
            matriculas = []
            for i in añosAsignatura:
                matriculas.append(i.Matriculados)

            x = np.array(range(0,añosUnicos.__len__())).reshape(-1,1)
            y = np.array(matriculas)
            modelo = LinearRegression().fit(x,y)

            precision = round(modelo.score(x,y),2)
            arrayPrecision.append(precision)

            # Creación de datos correspondientes a la generación de la gráfica
            puntosGrafica = matriculas
            for i in range(añosUnicos.__len__(),añosUnicos.__len__()+2):
                elemento = modelo.predict([[i]])
                puntosGrafica.append(elemento[0])

            elementoInfoGrafica = {}
            elementoInfoGrafica['label'] = asg.Nombre

            elementoInfoGrafica['data'] = puntosGrafica

            valorR = random.randint(0,255)
            valorG = random.randint(0,255)
            valorB = random.randint(0,255)
            elementoInfoGrafica['backgroundColor'] = 'rgba('+str(valorR)+','+str(valorG)+','+str(valorB)+', 0.2)'
            
            infoGrafica.append(elementoInfoGrafica)

            # Generación de tabla actual
            elementoTablaActual = {
                'Nombre':asg.Nombre,
                'Matriculados':añosAsignatura[añosAsignatura.__len__()-1].Matriculados,
                'GA':0,
                'GR':0,
                'Rat T':0,
                'Rat P':0
            }

            añoAsignaturaActual = añosAsignatura[añosAsignatura.__len__()-1]
            grupos = ObtenerGruposAño(añoAsignaturaActual.ID)
            elementoTablaActual['GA'] = grupos.__len__()

            gruposPequeños = 0
            for g in grupos:
                gruposPequeños += g.GruposReducidos

            elementoTablaActual['GR'] = gruposPequeños

            elementoTablaActual['Rat T'] = round(añosAsignatura[añosAsignatura.__len__()-1].Matriculados/grupos.__len__(), 2)
            elementoTablaActual['Rat P'] = round(añosAsignatura[añosAsignatura.__len__()-1].Matriculados/gruposPequeños, 2)

            # Generación de tabla predicción
            matriculadosFuturos = modelo.predict([[añosAsignatura.__len__()]])
            matriculadosFuturos = round(matriculadosFuturos[0])

            tablasActual.append(elementoTablaActual)

            elementoTablaPrediccion = {
                'Nombre':asg.Nombre,
                'Matriculados':matriculadosFuturos,
                'GA':elementoTablaActual['GA'],
                'GR':elementoTablaActual['GR'],
                'Rat T':0,
                'Rat P':0
            }

            elementoTablaPrediccion['Rat T'] = round(matriculadosFuturos/grupos.__len__(), 2)
            elementoTablaPrediccion['Rat P'] = round(matriculadosFuturos/gruposPequeños, 2)

            tablasPrediccion.append(elementoTablaPrediccion)

        listaDatosPrecisionNombre = zip(nombresAsignaturas,arrayPrecision)

        listaaños = [] 
        for j in añosUnicos:
            j = str(j)
            añoelemento = formatearAnio(j)
            listaaños.append(añoelemento)
        
        listaaños.append(añoProximo)
        listaaños.append(añoProximo2)

        listaaños.sort()

        return render(
            request,
            'resultadoprediccion.html',
            {
                'registrado':registrado,
                'listaDatos':listaDatosPrecisionNombre,
                'cursoProximo':añoProximo,
                'cursoActual':añoActual,
                'data':infoGrafica,
                'listaAños':listaaños,
                'tabla1':tablasActual,
                'tabla2':tablasPrediccion
            }
        )
