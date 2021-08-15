from .models import ObtenerElemento

# Función para comprobar si el usuario está registrado
def estaRegistrado(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

# Función para formatear un año academico de la siguiente manera: 
# 20xx/20xx+1
def formatearAnio(añoString):
    año1 = añoString[0] + añoString[1] + añoString[2] + añoString[3]
    año2 = añoString[4] + añoString[5] + añoString[6] + añoString[7]
    
    return año1 + "/" + año2

# Función para incluir un elemento dentro de una lista de asignaturas
# a la hora de generar el plan docente
def aniadeElementoPlanDocente(tablas, stringLista, elemento):
    if stringLista not in tablas:
        tablas[stringLista] = []
        tablas[stringLista].append(elemento)
    else:
        tablas[stringLista].append(elemento)

    return tablas

# Función para obtener el código de una mención en formato string
def obtenerCodigoMencion(idmencion):
    objmencion = ObtenerElemento("Mención",idmencion)
    return str(objmencion.Codigo)

# Función para establecer el string de tipo de una asignatura de 
# ingeniería informática
def defineTipoAsignaturaPlanDocenteInformatica(elemento,asignatura):
    if elemento['Tipo'] == 1:
        elemento['Tipo'] = "BAS"
    
    elif elemento['Tipo'] == 2:
        elemento['Tipo'] = "COM"

    elif elemento['Tipo'] == 3:
        mencion = obtenerCodigoMencion(asignatura.get('IDMencion_id'))

        if mencion == "01":
            elemento['Tipo'] = "CSI"
        elif mencion == "02":
            elemento['Tipo'] = "IC"
        elif mencion == "03":
            elemento['Tipo'] = "IS"
        elif mencion == "04":
            elemento['Tipo'] = "SI"
        elif mencion == "05":
            elemento['Tipo'] = "TI"

    elif elemento['Tipo'] == 4:
        elemento['Tipo'] = "OPT"
    
    return elemento

# Función para incluir una asignatura en una lista determinada 
# dependiendo del curso al que pertenezca
def aniadeAsignaturaInformaticaAPlanDocente(tablas, asig, elemento):
    if asig.get('Curso') == 1:
        aniadeElementoPlanDocente(tablas,'listaAsignaturas1',elemento)
    
    elif asig.get('Curso') == 2:
        aniadeElementoPlanDocente(tablas,'listaAsignaturas2',elemento)
    
    elif asig.get('Curso') == 3:
        mencion = obtenerCodigoMencion(asig.get('IDMencion_id'))

        if mencion == "00":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas3Comun',elemento)

        elif mencion == "01":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas3CSI',elemento)

        elif mencion == "02":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas3IC',elemento)

        elif mencion == "03":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas3IS',elemento)

        elif mencion == "04":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas3SI',elemento)

        elif mencion == "05":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas3TI',elemento)

    else:
        mencion = obtenerCodigoMencion(asig.get('IDMencion_id'))

        if mencion == "00":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas4PETFG',elemento)
            
        elif mencion == "01":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas4CSI',elemento)
            
        elif mencion == "02":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas4IC',elemento)
            
        elif mencion == "03":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas4IS',elemento)
            
        elif mencion == "04":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas4SI',elemento)
            
        elif mencion == "05":
            aniadeElementoPlanDocente(tablas,'listaAsignaturas4TI',elemento)

    return tablas

# Función para calcular la cantidad de grupos reducidos para una asignatura
# en un año determinado.
def numeroGruposReducidosEnAño(grupos):
    cantidad = 0

    for g in grupos:
        cantidad += g.GruposReducidos

    return cantidad
