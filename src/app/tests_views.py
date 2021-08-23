from django.test import TestCase

from .models import *

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
            Matriculados=2
        )
        AñoAsignatura.objects.create(
            PK=Asignatura.objects.get(PK="2961199424A60"),
            Año=20202021,
            Matriculados=2
        )
        AñoAsignatura.objects.create(
            PK=Asignatura.objects.get(PK="2961199424A60"),
            Año=20212022,
            Matriculados=2
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
        response = self.client.post('/plandocente/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['numerotablas'], '')
