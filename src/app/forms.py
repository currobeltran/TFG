from .models import *
from django.forms import ModelForm, PasswordInput, CharField, Form, FileField, ChoiceField, IntegerField, ModelChoiceField, FloatField, ModelMultipleChoiceField
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm
from allauth.account.utils import perform_login
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class ModelChoiceFieldEditado(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Nombre

class ModelMultipleChoiceFieldEditado(ModelMultipleChoiceField):
    def label_from_instance(self,obj):
        return obj.Nombre

class ModelChoiceAñoAsignatura(ModelChoiceField):
    def label_from_instance(self, obj):
        stringAño = str(obj.Año)
        añoFormateado = stringAño[0] + stringAño[1] + stringAño[2] + stringAño[3] + "/" + stringAño[4] + stringAño[5] + stringAño[6] + stringAño[7]

        return añoFormateado + " " + obj.PK.Nombre

class AsignaturaForm(ModelForm):
    class Meta:
        model = Asignatura
        fields = [
            'Nombre',
            'PKDif',
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

    CreditosGR = FloatField(label="Créditos grupo reducido")
    CreditosGA = FloatField(label="Créditos grupo amplio")
    Codigo = CharField(max_length=7,min_length=7)
    IDMencion = ModelChoiceFieldEditado(queryset=Mencion.objects, label="Mención")

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ['Nombre','Departamento','Acronimo','AsignaturaArea']
    
    AsignaturaArea = ModelMultipleChoiceFieldEditado(queryset=Asignatura.objects, label="Asignaturas del área")

class MencionForm(ModelForm):
    class Meta:
        model = Mencion
        fields = ['Codigo','Nombre']

class TituloForm(ModelForm):
    class Meta:
        model = Titulo
        fields = ['Codigo', 'Nombre', 'UmbralGR', 'UmbralGA', 'AsignaturaTitulo']
    
    AsignaturaTitulo = ModelMultipleChoiceFieldEditado(queryset=Asignatura.objects, label="Asignaturas del título")

class AñoAsignaturaForm(ModelForm):
    class Meta:
        model = AñoAsignatura
        fields = ['PK', 'Año', 'Matriculados']
    
    PK = ModelChoiceFieldEditado(queryset=Asignatura.objects, label="Asignatura")

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
    
    IDAñoAsignatura = ModelChoiceAñoAsignatura(queryset=AñoAsignatura.objects, label="Año universitario y asignatura al que pertenece el grupo")

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

class EditarUsuarioForm(Form):
    nuevo_nombre_de_usuario = CharField(max_length=100)
    nueva_contraseña = CharField(
            validators=[
                RegexValidator(r'^[0-9a-zA-Z@#$%^&+=/-_*!"·]{12,}$',
                        message="La contraseña debe tener 12 caracteres, un número y uno de los siguientes caracteres: @#$%^&+=/-_*!\"·"
                    )
                ],
            widget=PasswordInput
        )
    confirmar_contraseña = CharField(widget=PasswordInput)

    def clean_confirmar_contraseña(self):
        nueva_contraseña = self.cleaned_data.get('nueva_contraseña')
        confirmar_contraseña = self.cleaned_data.get('confirmar_contraseña')

        if nueva_contraseña != confirmar_contraseña and nueva_contraseña:
            raise ValidationError("Las contraseñas no coinciden")

        return self.cleaned_data

class SubirArchivoDatos(Form):
    archivo = FileField(label="Suba aquí su archivo de datos")
    opcion = ChoiceField(choices=(
                            (1,"Añadir asignaturas"),
                            (2,"Añadir años académicos de asignaturas")
                        ), label="Elija una opción")
