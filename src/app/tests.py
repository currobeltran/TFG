from django.test import TestCase

from .models import *

class AsignaturaModelTests(TestCase):
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

    def test_asignaturaEditada(self):
        asg = Asignatura.objects.get(PK="2961199424A60")
        ModificaAsignatura(
            id=asg.PK,
            pkdif=1,
            nombre=asg.Nombre,
            acronimo=asg.Acronimo,
            creditosgr=asg.CreditosGR,
            creditosga=asg.CreditosGA,
            idasiganterior=0,
            curso=asg.Curso,
            codigo=asg.Codigo,
            semestre=asg.Semestre,
            tipoasig=asg.TipoAsignatura,
            idmencion=1
        )

        nuevaAsg = Asignatura.objects.get(PK="2961199424A61")

        self.assertEqual(ObtenerElemento("Asignatura","2961199424A60"), '')
        self.assertEqual("2961199424A61", nuevaAsg.PK)
