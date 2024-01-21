from django.shortcuts import render
from .models import Alumno, Nota
from datetime import datetime

def vista_todos_alumnos(request):
    alumnos = Alumno.objects.all()
    resultados = []

    # Definición de las fechas de cada progreso
    progreso1_inicio = datetime(2023, 3, 10)
    progreso1_fin = datetime(2023, 11, 25)
    progreso2_inicio = datetime(2023, 11, 30)
    progreso2_fin = datetime(2024, 1, 6)

    for alumno in alumnos:
        # Calcula la nota promedio para Progreso 1 y la convierte en porcentaje del 25%
        notas_progreso1 = Nota.objects.filter(alumno=alumno, fecha__range=(progreso1_inicio, progreso1_fin))
        promedio_progreso1 = sum(nota.valor for nota in notas_progreso1) / len(notas_progreso1) if notas_progreso1.exists() else 0
        porcentaje_progreso1 = promedio_progreso1 * 0.25  # Convierte a porcentaje de la nota final

        # Calcula la nota promedio para Progreso 2 y la convierte en porcentaje del 35%
        notas_progreso2 = Nota.objects.filter(alumno=alumno, fecha__range=(progreso2_inicio, progreso2_fin))
        promedio_progreso2 = sum(nota.valor for nota in notas_progreso2) / len(notas_progreso2) if notas_progreso2.exists() else 0
        porcentaje_progreso2 = promedio_progreso2 * 0.35  # Convierte a porcentaje de la nota final

        # Calcula el total de porcentaje acumulado con Progresos 1 y 2
        total_porcentaje_acumulado = porcentaje_progreso1 + porcentaje_progreso2

        # Determina el porcentaje necesario en el Progreso 3 para alcanzar la nota de aprobación
        porcentaje_necesario_progreso3 = 6 - total_porcentaje_acumulado  # Porcentaje que falta para llegar al 60%


        # Añade el resultado al alumno
        resultado_alumno = {
            'alumno': alumno,
            'nota_progreso1': f"{porcentaje_progreso1:.1f}",
            'nota_progreso2': f"{porcentaje_progreso2:.1f}",
            'nota_necesaria_progreso3': f"{porcentaje_necesario_progreso3:.1f}"
        }
        resultados.append(resultado_alumno)

    return render(request, 'vista_nota_necesaria.html', {'resultados': resultados})




def main_page(request):
    return render(request, 'index.html')