from .models import *
from django.forms import ModelForm

class AsignaturaForm(ModelForm):
    class Meta:
        model = Asignatura
        fields = [
            'Nombre',
            'Acronimo',
            'CreditosGR',
            'CreditosGA',
            'IdAsignaturaAnterior',
            'Curso',
            'Codigo',
            'Semestre',
            'TipoAsignatura',
            'IDMencion',
        ]

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ['Nombre','Departamento','Acronimo','AsignaturaArea']

class MencionForm(ModelForm):
    class Meta:
        model = Mencion
        fields = ['Codigo','Nombre']

class TituloForm(ModelForm):
    class Meta:
        model = Titulo
        fields = ['Codigo', 'Nombre', 'UmbralGR', 'UmbralGA', 'AsignaturaTitulo']

class AñoAsignaturaForm(ModelForm):
    class Meta:
        model = AñoAsignatura
        fields = ['PK', 'Año', 'Matriculados']

class GrupoForm(ModelForm):
    class Meta:
        model = Grupo
        fields = [
            'IDAñoAsignatura',
            'Letra',
            'Nuevos',
            'Repetidores',
            'Retenidos',
            'Plazas',
            'LibreConfiguracion',
            'OtrosTitulos',
            'Asimilado',
            'Compartido',
            'Turno',
            'GruposReducidos',
        ]
