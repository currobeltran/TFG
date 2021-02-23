from django.contrib import admin
from .models import Asignatura, Area, Mencion, Titulo, AñoAsignatura, Grupo

# Register your models here.
admin.site.register(Asignatura)
admin.site.register(Area)
admin.site.register(Mencion)
admin.site.register(Titulo)
admin.site.register(AñoAsignatura)
admin.site.register(Grupo)