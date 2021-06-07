from django.db import models
from django.http import JsonResponse
from django.contrib.auth.models import User
import math
import django_tables2 as tables

class Asignatura(models.Model):
    OPCIONES_TIPO_ASIGNATURA = [
        (1, 'Básica'),
        (2, 'Común'),
        (3, 'Obligatoria de Mención'),
        (4, 'Optativa'),
        (5, 'Trabajo de Fin de Grado'),
        (6, 'Prácticas de Empresa'),
    ]
    
    PK = models.CharField(primary_key=True, max_length=13)
    PKDif = models.IntegerField(blank=True)
    Nombre = models.CharField(max_length=100)
    Acronimo = models.CharField(max_length=3, blank=True)
    CreditosGR = models.FloatField()
    CreditosGA = models.FloatField()
    IdAsignaturaAnterior = models.IntegerField(blank=True)
    Curso = models.IntegerField()
    Codigo = models.CharField(max_length=7)
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
    Codigo = models.CharField(max_length=2)
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

    elif tabla == "Año asignatura":
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

def ObtenerAñoAsignaturaUnico(pk,curso):
    return AñoAsignatura.objects.get(PK=pk,Año=curso)

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
    añosasig = ''

    try:
        añosasig = AñoAsignatura.objects.get(PK=pk,Año=año)
    except:
        print("Consulta inexistente")
        
    if añosasig == '':
        return False
    else:
        return añosasig

def AsignaturaTieneAño(pk,año):
    añosasig = ''

    try:
        añosasig = AñoAsignatura.objects.get(PK=pk,Año=año)
    except:
        print("Consulta inexistente")
        
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
        infoaño = {}

        for a in años:
            objaño = AsignaturaTieneAño(asgaux,a) 
            
            if objaño != False:
                gr = ObtenerGruposAño(objaño.ID)
                infoaño['NumeroGA'] = len(gr)
                
                numeroGR = 0
                for x in gr:
                    numeroGR += x.GruposReducidos
                infoaño['NumeroGR'] = numeroGR
                infoaño['NumeroMatriculados'] = objaño.Matriculados
                
                if(infoaño['NumeroGA'] != 0):
                    infoaño['RatioGA'] = '%.3f'%(objaño.Matriculados/infoaño['NumeroGA'])
                else:
                    infoaño['RatioGA'] = 0
                
                if(infoaño['NumeroGR'] != 0):
                    infoaño['RatioGR'] = '%.3f'%(objaño.Matriculados/infoaño['NumeroGR'])
                else:
                    infoaño['RatioGR'] = 0


        ret[asgaux.Nombre] = {
            'Nombre':asgaux.Nombre,
            'PK':asgaux.PK,
            'Acronimo':asgaux.Acronimo,
            'Creditos Grupo Amplio':asgaux.CreditosGA,
            'Creditos Grupo Reducido':asgaux.CreditosGR,
            'Curso':asgaux.Curso,
            'Semestre':asgaux.Semestre,
            'Tipo de Asignatura':asgaux.TipoAsignatura,
            'InfoAño':infoaño,
        }

    return ret

def EditarUsuario(username, nuevousername, nuevacontraseña):
    user = User.objects.get(username=username)

    user.username = nuevousername
    user.set_password(nuevacontraseña)
    user.save()

    return user

def CrearAsignatura(nombre,pkdif,acronimo,creditosgr,creditosga,idasiganterior,curso,codigo,semestre,tipoasig,idmencion):
    mencion = ObtenerElemento("Mención", idmencion)
    
    titulo = codigo[0]+codigo[1]+codigo[2]
    plan = codigo[3]+codigo[4]
    idcodigo = codigo[5]+codigo[6]

    pk = titulo + plan + mencion.Codigo + str(curso) + str(semestre) + str(tipoasig) + idcodigo + str(pkdif)

    n = Asignatura(PK=pk,PKDif=pkdif,Nombre=nombre,Acronimo=acronimo,CreditosGR=creditosgr,CreditosGA=creditosga,IdAsignaturaAnterior=idasiganterior,
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

    return n.ID

def CrearGrupo(idañoasig,letra,nuevos,repetidores,retenidos,plazas,libreconf,otrostitulos,turno,gruposred,asimilado=0,compartido=0):
    añoasig = ObtenerElemento("Año asignatura", idañoasig)

    n = Grupo(
        IDAñoAsignatura=añoasig,
        Letra=letra,
        Nuevos=nuevos,
        Repetidores=repetidores,
        Retenidos=retenidos,
        Plazas=plazas,
        LibreConfiguracion=libreconf,
        OtrosTitulos=otrostitulos,
        Asimilado=asimilado,
        Compartido=compartido,
        Turno=turno,
        GruposReducidos=gruposred
    )
    n.save()

def ModificaAsignatura(id,pkdif,nombre,acronimo,creditosgr,creditosga,idasiganterior,curso,codigo,semestre,tipoasig,idmencion):
    mencion = ObtenerElemento("Mención", idmencion)
    
    titulo = codigo[0]+codigo[1]+codigo[2]
    plan = codigo[3]+codigo[4]
    idcodigo = codigo[5]+codigo[6]

    pk = titulo + plan + mencion.Codigo + str(curso) + str(semestre) + str(tipoasig) + idcodigo + str(pkdif)

    asig = Asignatura.objects.get(pk=id)
    asig.Nombre = nombre
    asig.Acronimo = acronimo
    asig.CreditosGR = creditosgr
    asig.CreditosGA = creditosga
    asig.IdAsignaturaAnterior = idasiganterior
    asig.Curso = curso
    asig.Codigo = codigo
    asig.Semestre = semestre
    asig.TipoAsignatura = tipoasig
    asig.IDMencion = mencion
    asig.PK = pk

    asig.save()

def ModificaMencion(id,codigo,nombre):
    mencion = Mencion.objects.get(ID=id)
    mencion.Codigo = codigo
    mencion.Nombre = nombre

    mencion.save()

def ModificaTitulo(id,codigo,nombre,umbralga,umbralgr,asignaturatitulo):
    titulo = Titulo.objects.get(ID=id)

    titulo.Codigo = codigo
    titulo.Nombre = nombre
    titulo.UmbralGA = umbralga
    titulo.UmbralGR = umbralgr
    titulo.AsignaturaTitulo.set(asignaturatitulo)

    titulo.save()

def ModificaArea(id,nombre,departamento,acronimo,asignaturaarea):
    area = Area.objects.get(ID=id)

    area.Nombre = nombre
    area.Departamento = departamento
    area.Acronimo = acronimo
    area.AsignaturaArea.set(asignaturaarea)

    area.save()

def ModificaAñoAsignatura(id,pk,año,matriculados):
    añoasig = AñoAsignatura.objects.get(ID=id)
    asig = ObtenerElemento("Asignatura",pk)

    añoasig.PK = asig
    añoasig.Año = año
    añoasig.Matriculados = matriculados

    añoasig.save()

def ModificaGrupo(id,idañoasig,letra,nuevos,repetidores,retenidos,plazas,libreconf,otrostitulos,turno,gruposred,asimilado=0,compartido=0):
    grupo = Grupo.objects.get(ID=id)
    añoasig = ObtenerElemento("Año asignatura",idañoasig)

    grupo.IDAñoAsignatura = añoasig
    grupo.Letra = letra
    grupo.Nuevos = nuevos
    grupo.Repetidores = repetidores
    grupo.Retenidos = retenidos
    grupo.Plazas = plazas
    grupo.LibreConfiguracion = libreconf
    grupo.OtrosTitulos = otrostitulos
    grupo.Turno = turno
    grupo.GruposReducidos = gruposred
    grupo.Asimilado = asimilado
    grupo.Compartido = compartido

    grupo.save()

def EliminaObjeto(id,tabla):
    elemento = ObtenerElemento(tabla,id)
    elemento.delete()

def CrearAsignaturaDesdeCSV(nombre,pkdif,acr,crgr,crga,idasiganterior,curso,codigo,semestre,tipoasig,idmencion):
    CrearAsignatura(
        nombre=nombre,
        pkdif=pkdif,
        acronimo=acr,
        creditosgr=crgr,
        creditosga=crga,
        idasiganterior=idasiganterior,
        curso=curso,
        codigo=codigo,
        semestre=semestre,
        tipoasig=tipoasig,
        idmencion=idmencion
    )

def RecalculoDeMatriculados(idañoasig):
    grupos = ObtenerGruposAño(idañoasig)
    matriculadosTotales = 0

    for x in grupos:
        matriculadosTotales += (x.Nuevos + x.Repetidores + x.Retenidos + x.LibreConfiguracion + x.OtrosTitulos)
    
    return matriculadosTotales

def ModificaMatriculadosAñoAsignatura(id, matriculados):
    añoasig = AñoAsignatura.objects.get(ID=id)

    añoasig.Matriculados = matriculados

    añoasig.save()

class TablaAsignatura(tables.Table):
    Nombre = tables.Column()
    Acronimo = tables.Column(verbose_name="Acrónimo")
    CreditosGA = tables.Column(verbose_name="Créditos GA")
    CreditosGR = tables.Column(verbose_name="Créditos GR")
    Semestre = tables.Column()
    TipoAsignatura = tables.Column(verbose_name="Tipo de Asignatura")
    AL_Anteriores = tables.Column(verbose_name="Alumnos curso anterior")
    AL_Actuales = tables.Column(verbose_name="Alumnos curso actual")
    GA = tables.Column(verbose_name="Grupos amplios")
    GR = tables.Column(verbose_name="Grupos reducidos")
    Rat_T = tables.Column(verbose_name="Ratio Teoría")
    Rat_P = tables.Column(verbose_name="Ratio Prácticas")

    class Meta:
        template_name="django_tables2/bootstrap.html"
