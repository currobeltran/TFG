from .models import *
from django.forms import ModelForm, PasswordInput
from allauth.account.forms import LoginForm
from allauth.account.utils import perform_login

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

class LoginFormPersonalizado(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginFormPersonalizado, self).__init__(*args, **kwargs)

        # La intención es que no aparezca el tic "recuerdame" en el formulario de login
        # ya que no lo vamos a utilizar en principio
        if 'remember' in self.fields.keys():
            self.fields.pop('remember')
    
    # Nueva función que se llevará a cabo al hacer login en la aplicación, en sustitución de
    # la anterior que realizaba por defecto el plugin django allauth y que necesitaba del
    # campo anteriormente eliminado 'remember'
    def login(self, request, redirect_url=None):
        ret = perform_login(
            request,
            self.user,
            email_verification=None,
            redirect_url=redirect_url,
        )
        
        return ret
