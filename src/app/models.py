from django.db import models
from django.http import JsonResponse
from django.contrib.auth.models import User
import math

class Asignatura(models.Model):
    OPCIONES_TIPO_ASIGNATURA = [
        (1, 'Básica'),
        (2, 'Común'),
        (3, 'Obligatoria de Mención'),
        (4, 'Optativa'),
        (5, 'Trabajo de Fin de Grado'),
        (6, 'Prácticas de Empresa'),
    ]
    
    PK = models.IntegerField(primary_key=True)
    PKDif = models.IntegerField(blank=True)
    Nombre = models.CharField(max_length=100)
    Acronimo = models.CharField(max_length=3, blank=True)
    CreditosGR = models.IntegerField()
    CreditosGA = models.IntegerField()
    IdAsignaturaAnterior = models.IntegerField(blank=True)
    Curso = models.IntegerField()
    Codigo = models.IntegerField()
    Semestre = models.IntegerField()
    TipoAsignatura = models.IntegerField(choices=OPCIONES_TIPO_ASIGNATURA)
    IDMencion = models.ForeignKey('Mencion', on_delete=models.CASCADE)

class Area(models.Model):
    ID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100)
    Departamento = models.CharField(max_length=100)
    Acronimo = models.CharField(max_length=3, blank=True)
    AsignaturaArea = models.ManyToManyField('Asignatura')

class Mencion(models.Model):
    ID = models.AutoField(primary_key=True)
    Codigo = models.IntegerField()
    Nombre = models.CharField(max_length=100)

class Titulo(models.Model):
    ID = models.AutoField(primary_key=True)
    Codigo = models.IntegerField()
    Nombre = models.CharField(max_length=100)
    UmbralGA = models.FloatField()
    UmbralGR = models.FloatField()
    AsignaturaTitulo = models.ManyToManyField('Asignatura')

class AñoAsignatura(models.Model):
    ID = models.AutoField(primary_key=True)
    PK = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    Año = models.IntegerField()
    Matriculados = models.IntegerField()

class Grupo(models.Model):
    TURNOS_DE_GRUPO = [
        ('M', 'Mañana'),
        ('T', 'Tarde'),
    ]
    
    ID = models.AutoField(primary_key=True)
    IDAñoAsignatura = models.ForeignKey(AñoAsignatura, on_delete=models.CASCADE)
    Letra = models.CharField(max_length=1)
    Nuevos = models.IntegerField()
    Repetidores = models.IntegerField()
    Retenidos = models.IntegerField()
    Plazas = models.IntegerField()
    LibreConfiguracion = models.IntegerField()
    OtrosTitulos = models.IntegerField()
    Asimilado = models.IntegerField(blank=True)
    Compartido = models.IntegerField(blank=True)
    Turno = models.CharField(max_length=1, choices=TURNOS_DE_GRUPO)
    GruposReducidos = models.IntegerField()

def ObtenerRegistros(tabla):
    ret = []

    if tabla == "Asignatura":
        x = Asignatura.objects.all()
        for i in x:
            ret.append({'id':i.PK, 'nombre':i.Nombre})
        return ret

    elif tabla == "Área":
        x = Area.objects.all()
        for i in x:
            ret.append({'id':i.ID, 'nombre':i.Nombre})
        return ret

    elif tabla == "Mención":
        x = Mencion.objects.all()
        for i in x:
            ret.append({'id':i.ID, 'nombre':i.Nombre})
        return ret

    elif tabla == "Título":
        x = Titulo.objects.all()
        for i in x:
            ret.append({'id':i.ID, 'nombre':i.Nombre})
        return ret

    elif tabla == "Año Asignatura":
        x = AñoAsignatura.objects.all()
        for i in x:
            ret.append({'id':i.ID, 'nombre':i.Año})
        return ret

    elif tabla == "Grupo":
        x = Grupo.objects.all()
        for i in x:
            ret.append({'id':i.ID, 'nombre':i.Letra})
        return ret

    return ret

def ObtenerElemento(tabla, id):
    if tabla == "Asignatura":
        x = Asignatura.objects.get(PK=id)
        return x

    elif tabla == "Área":
        x = Area.objects.get(ID=id)
        return x

    elif tabla == "Mención":
        x = Mencion.objects.get(ID=id)
        return x

    elif tabla == "Título":
        x = Titulo.objects.get(ID=id)
        return x

    elif tabla == "Año asignatura":
        x = AñoAsignatura.objects.get(ID=id)
        return x

    elif tabla == "Grupo":
        x = Grupo.objects.get(ID=id)
        return x

    return ''

def ObtenerAñosUnicos():
    ret = []
    x = AñoAsignatura.objects.all()
    
    for i in x:
        ret.append(i.Año)

    unico = list(dict.fromkeys(ret))

    return unico

def ObtenerAtributosTabla(tabla):
    ret = []

    if tabla == "Asignatura":
        x = Asignatura._meta.get_fields()
        for i in x:
            nombre = i.name
            ret.append(nombre)
        return ret

    elif tabla == "Área":
        x = Area._meta.get_fields()
        for i in x:
            nombre = i.name
            ret.append(nombre)
        return ret

    elif tabla == "Mención":
        x = Mencion._meta.get_fields()
        for i in x:
            nombre = i.name
            ret.append(nombre)
        return ret

    elif tabla == "Título":
        x = Titulo._meta.get_fields()
        for i in x:
            nombre = i.name
            ret.append(nombre)
        return ret

    elif tabla == "Año Asignatura":
        x = AñoAsignatura._meta.get_fields()
        for i in x:
            nombre = i.name
            ret.append(nombre)
        return ret

    elif tabla == "Grupo":
        x = Grupo._meta.get_fields()
        for i in x:
            nombre = i.name
            ret.append(nombre)
        
        ret.remove("ID")
        ret.remove("IDAñoAsignatura")
        return ret

    return ret

def ObtenerAñosAsignatura(pk):
    ret = AñoAsignatura.objects.filter(PK=pk)
    listaret = []

    for x in ret:
        listaret.append(x)
    
    return listaret

def AsignaturaTieneAño(asig,año):
    pk = asig.PK
    añosasig = AñoAsignatura.objects.get(PK=pk,Año=año)

    if añosasig == '':
        return False
    else:
        return añosasig

def ObtenerGruposAño(idaño):
    ret = []
    q = Grupo.objects.filter(IDAñoAsignatura=idaño)

    for x in q:
        ret.append(x)

    return ret

def ObtenerValorInfo(info,gr):
    if info == "Nuevos":
        return gr.Nuevos
    elif info == "Repetidores":
        return gr.Repetidores
    elif info == "Retenidos":
        return gr.Retenidos
    elif info == "Plazas":
        return gr.Plazas
    elif info == "LibreConfiguracion":
        return gr.LibreConfiguracion
    elif info == "OtrosTitulos":
        return gr.OtrosTitulos
    elif info == "Asimilado":
        return gr.Asimilado
    elif info == "Compartido":
        return gr.Compartido
    elif info == "Turno":
        return gr.Turno
    elif info == "GruposReducidos":
        return gr.GruposReducidos

    return False

def ConsultaBusquedaBBDD(asig,años,info):
    ret = {}

    for x in asig:
        asgaux = ObtenerElemento("Asignatura",x)
        añosasig = ObtenerAñosAsignatura(asgaux.PK)
        grupos = {}

        for a in años:
            objaño = AsignaturaTieneAño(asgaux,a) 
            
            if objaño != False:
                gr = ObtenerGruposAño(objaño.ID)
                for x in gr:
                    key = x.Letra + " " + objaño.Año.__str__()
                    grupos[key] = {'Año Academico':objaño.Año.__str__(),'Letra':x.Letra}
                    for i in info:
                        if ObtenerValorInfo(i,x) != False:
                            grupos[key][i] = ObtenerValorInfo(i,x)

        ret[asgaux.Nombre] = {
            'Nombre':asgaux.Nombre,
            'PK':asgaux.PK,
            'Acronimo':asgaux.Acronimo,
            'Creditos Grupo Amplio':asgaux.CreditosGA,
            'Creditos Grupo Reducido':asgaux.CreditosGR,
            'Curso':asgaux.Curso,
            'Semestre':asgaux.Semestre,
            'Tipo de Asignatura':asgaux.TipoAsignatura,
            'Grupos':grupos,
        }

    return ret

def EditarUsuario(username, nuevousername, nuevacontraseña):
    user = User.objects.get(username=username)

    user.username = nuevousername
    user.set_password(nuevacontraseña)
    user.save()

    return user

def CrearAsignatura(nombre,acronimo,creditosgr,creditosga,idasiganterior,curso,codigo,semestre,tipoasig,idmencion):
    mencion = ObtenerElemento("Mención", idmencion)
    titulo = math.floor(codigo/10000)
    plan = math.floor((codigo-titulo*10000)/100)
    idcodigo = (codigo - titulo*10000 - plan*100)

    pk = idcodigo*10 + tipoasig*1000 + semestre*10000 + curso*100000 + mencion.Codigo*1000000 + plan*100000000 + titulo*10000000000
    n = Asignatura(PK=pk,PKDif=0,Nombre=nombre,Acronimo=acronimo,CreditosGR=creditosgr,CreditosGA=creditosga,IdAsignaturaAnterior=idasiganterior,
    Curso=curso,Codigo=codigo,Semestre=semestre,TipoAsignatura=tipoasig,IDMencion=mencion)

    n.save()

def CrearMencion(codigo,nombre):
    n = Mencion(Codigo=codigo,Nombre=nombre)
    n.save()

def CrearTitulo(codigo,nombre,umbralga,umbralgr,asignaturatitulo):
    n = Titulo(Codigo=codigo,Nombre=nombre,UmbralGA=umbralga,UmbralGR=umbralgr)
    n.save()

    n.AsignaturaTitulo.set(asignaturatitulo)
    n.save()

def CrearArea(nombre,departamento,acronimo,asignaturaarea):
    n = Area(Nombre=nombre,Departamento=departamento,Acronimo=acronimo)
    n.save()

    n.AsignaturaArea.set(asignaturaarea)
    n.save()

def CrearAñoAsignatura(pk,año,matriculados):
    asig = ObtenerElemento("Asignatura",pk)

    n = AñoAsignatura(PK=asig,Año=año,Matriculados=matriculados)
    n.save()
