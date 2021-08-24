from django.test import TestCase
import json

from .models import *

# Tests para comprobar que la información solicitada a 
# alguna de las vistas de visualización de información 
# funcionan correctamente.
class BusquedaDeDatosTest(TestCase):
    def setUp(self):
        Mencion.objects.create(
            Codigo=99,
            Nombre="Mención de prueba"
        )
        Asignatura.objects.create(
            PK="2961199424A60",
            PKDif=0,
            Nombre="Derecho Informático",
            Acronimo="DI",
            CreditosGR=3.0,
            CreditosGA=3.0,
            IdAsignaturaAnterior=0,
            Curso=4,
            Codigo="29611A6",
            Semestre=2,
            TipoAsignatura=4,
            IDMencion=Mencion.objects.get(Codigo=99)
        )
        AñoAsignatura.objects.create(
            PK=Asignatura.objects.get(PK="2961199424A60"),
            Año=20192020,
            Matriculados=3
        )
        AñoAsignatura.objects.create(
            PK=Asignatura.objects.get(PK="2961199424A60"),
            Año=20202021,
            Matriculados=3
        )
        AñoAsignatura.objects.create(
            PK=Asignatura.objects.get(PK="2961199424A60"),
            Año=20212022,
            Matriculados=3
        )
        Grupo.objects.create(
            IDAñoAsignatura=AñoAsignatura.objects.get(Año=20192020),
            Letra="A",
            Nuevos=1,
            Repetidores=2,
            Retenidos=0,
            Plazas=2,
            LibreConfiguracion=0,
            OtrosTitulos=0,
            Asimilado=0,
            Compartido=0,
            Turno="M",
            GruposReducidos=1
        )
        Grupo.objects.create(
            IDAñoAsignatura=AñoAsignatura.objects.get(Año=20202021),
            Letra="A",
            Nuevos=1,
            Repetidores=2,
            Retenidos=0,
            Plazas=2,
            LibreConfiguracion=0,
            OtrosTitulos=0,
            Asimilado=0,
            Compartido=0,
            Turno="M",
            GruposReducidos=1
        )
        Grupo.objects.create(
            IDAñoAsignatura=AñoAsignatura.objects.get(Año=20212022),
            Letra="A",
            Nuevos=1,
            Repetidores=2,
            Retenidos=0,
            Plazas=2,
            LibreConfiguracion=0,
            OtrosTitulos=0,
            Asimilado=0,
            Compartido=0,
            Turno="M",
            GruposReducidos=1
        )
    
    def test_Tablas(self):
        response = self.client.post('/buscadorBBDD',{
                'asignaturas[]':['2961199424A60'],
                'añoacademico[]':[20192020],
                'info[]':['Letra','Nuevos','Repetidores'],
                'customRadio':['tabla']
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['listadatos'][0]['tabla'][0]['Letra'], "A")
        self.assertEqual(response.context['listadatos'][0]['tabla'][0]['Nuevos'], 1)
        self.assertEqual(response.context['listadatos'][0]['tabla'][0]['Repetidores'], 2)

    def test_Grafica(self):
        response = self.client.post('/buscadorBBDD',{
                'asignaturas[]':['2961199424A60'],
                'añoacademico[]':[20192020],
                'info[]':['Nuevos','Repetidores'],
                'customRadio':['grafica']
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['data'][0]['data'],[1])
        self.assertEqual(response.context['data'][1]['data'],[2])
    
    def test_PlanDocente(self):
        response = self.client.get('/plandocente/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['AlumnosActualesactual'], 3)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['GruposGrandesactual'], 1)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['GruposReducidosactual'], 1)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['RatioTeoriaactual'], 3)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['RatioPracticasactual'], 3)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['Diferencia'], 0)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['IncrementoTeoria'], 0)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['IncrementoPractica'], 0)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['IncrementoTotal'], 0)
        self.assertEqual(response.context['tablas']['listaAsignaturas4Comunes'][0]['Creditos'], 6)

# Test para comprobar que la funcionalidad de 
# realizar predicciones y la operación de regresión lineal
# es correcta. Utilizamos datos distintos a los de la clase
# BusquedaDeDatosTest para comprobar la correcta realización 
# de la regresión lineal
class TestPredicciones(TestCase):
    def setUp(self):
        Mencion.objects.create(
            Codigo=99,
            Nombre="Mención de prueba"
        )
        Asignatura.objects.create(
            PK="2961199424A60",
            PKDif=0,
            Nombre="Derecho Informático",
            Acronimo="DI",
            CreditosGR=3.0,
            CreditosGA=3.0,
            IdAsignaturaAnterior=0,
            Curso=4,
            Codigo="29611A6",
            Semestre=2,
            TipoAsignatura=4,
            IDMencion=Mencion.objects.get(Codigo=99)
        )
        AñoAsignatura.objects.create(
            PK=Asignatura.objects.get(PK="2961199424A60"),
            Año=20192020,
            Matriculados=3
        )
        AñoAsignatura.objects.create(
            PK=Asignatura.objects.get(PK="2961199424A60"),
            Año=20202021,
            Matriculados=4
        )
        AñoAsignatura.objects.create(
            PK=Asignatura.objects.get(PK="2961199424A60"),
            Año=20212022,
            Matriculados=5
        )
        Grupo.objects.create(
            IDAñoAsignatura=AñoAsignatura.objects.get(Año=20192020),
            Letra="A",
            Nuevos=1,
            Repetidores=2,
            Retenidos=0,
            Plazas=2,
            LibreConfiguracion=0,
            OtrosTitulos=0,
            Asimilado=0,
            Compartido=0,
            Turno="M",
            GruposReducidos=1
        )
        Grupo.objects.create(
            IDAñoAsignatura=AñoAsignatura.objects.get(Año=20202021),
            Letra="A",
            Nuevos=2,
            Repetidores=2,
            Retenidos=0,
            Plazas=2,
            LibreConfiguracion=0,
            OtrosTitulos=0,
            Asimilado=0,
            Compartido=0,
            Turno="M",
            GruposReducidos=1
        )
        Grupo.objects.create(
            IDAñoAsignatura=AñoAsignatura.objects.get(Año=20212022),
            Letra="A",
            Nuevos=5,
            Repetidores=2,
            Retenidos=0,
            Plazas=2,
            LibreConfiguracion=0,
            OtrosTitulos=0,
            Asimilado=0,
            Compartido=0,
            Turno="M",
            GruposReducidos=1
        )

    def test_predicciones(self):
        response = self.client.post('/predicciones',{
            'asignaturas[]':['2961199424A60']
        })

        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(response.context['data'][0]['data'][3], 6)
        self.assertAlmostEqual(response.context['data'][0]['data'][4], 7)

# Tests para los distintos métodos utilizados a la hora de
# realizar una consulta en AJAX
class MetodosAJAXTests(TestCase):
    def setUp(self):
        Mencion.objects.create(
            Codigo=99,
            Nombre="Mención de prueba"
        )
        Asignatura.objects.create(
            PK="2961199424A60",
            PKDif=0,
            Nombre="Derecho Informático",
            Acronimo="DI",
            CreditosGR=3.0,
            CreditosGA=3.0,
            IdAsignaturaAnterior=0,
            Curso=4,
            Codigo="29611A6",
            Semestre=2,
            TipoAsignatura=4,
            IDMencion=Mencion.objects.get(Codigo=99)
        )
    
    def test_buscaRegistrosBBDD(self):
        response = self.client.get('/api/buscarBBDD?tipo=Asignatura')

        self.assertEqual(response.status_code, 200)
        contentJson = json.loads(response.content.decode("utf-8"))
        self.assertEqual(contentJson['0']['id'], '2961199424A60')
        self.assertEqual(contentJson['0']['nombre'], 'Derecho Informático')

    def test_buscaAsignaturasSemestre(self):
        response = self.client.get('/api/buscarAsignaturaSemestre?semestre=8')

        self.assertEqual(response.status_code, 200)
        contentJson = json.loads(response.content.decode("utf-8"))
        self.assertEqual(contentJson['0']['PK'], '2961199424A60')
        self.assertEqual(contentJson['0']['Nombre'], 'Derecho Informático')
