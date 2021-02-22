from django.db import models


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
