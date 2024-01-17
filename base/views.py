from django.shortcuts import render
from .models import Alimento, PerfilNutricional, RegistroDiario, AlimentoNutriente
from django.contrib.auth.decorators import login_required
from .utils import calcular_necesidades_nutricionales, analizar_ingesta_nutricional, calcular_bmr, ha_cumplido_limites
from datetime import date, datetime
from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404


# Analiza el consumo nutricional de todos los perfiles, agrupándolos en menores de 30 años y mayores o iguales a 30 años.
# Para cada grupo, calcula la suma total de calorías, proteínas, carbohidratos, grasas y nutrientes consumidos
# y luego calcula el promedio por usuario en cada grupo.
def analisis_consumo(fecha_inicio=None, fecha_fin=None):
    # Convertir fechas de string a objetos datetime si son proporcionadas
    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None

    perfiles = PerfilNutricional.objects.all()
    resultados = {
        'menores_30': {'calorias': 0, 'proteinas': 0, 'carbohidratos': 0, 'grasas': 0, 'nutrientes': {}},
        'mayores_30': {'calorias': 0, 'proteinas': 0, 'carbohidratos': 0, 'grasas': 0, 'nutrientes': {}}
    }

    for perfil in perfiles:
        grupo = 'menores_30' if perfil.edad < 30 else 'mayores_30'
        # Filtrar los registros por usuario y fechas si se proporcionan
        registros = RegistroDiario.objects.filter(usuario=perfil.usuario)
        if fecha_inicio:
            registros = registros.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            registros = registros.filter(fecha__lte=fecha_fin)

        for registro in registros:
            alimento = registro.alimento
            resultados[grupo]['calorias'] += float(alimento.calorias) * float(registro.cantidad)
            resultados[grupo]['proteinas'] += float(alimento.proteinas) * float(registro.cantidad)
            resultados[grupo]['carbohidratos'] += float(alimento.carbohidratos) * float(registro.cantidad)
            resultados[grupo]['grasas'] += float(alimento.grasas) * float(registro.cantidad)

            nutrientes = AlimentoNutriente.objects.filter(alimento=alimento)
            for nutriente in nutrientes:
                if nutriente.nutriente.nombre not in resultados[grupo]['nutrientes']:
                    resultados[grupo]['nutrientes'][nutriente.nutriente.nombre] = 0
                resultados[grupo]['nutrientes'][nutriente.nutriente.nombre] += float(nutriente.cantidad) * float(registro.cantidad)

    # Calcular promedios
    for grupo in resultados:
        total_usuarios = PerfilNutricional.objects.filter(edad__lt=30).count() if grupo == 'menores_30' else PerfilNutricional.objects.filter(edad__gte=30).count()
        if total_usuarios > 0:
            for key in ['calorias', 'proteinas', 'carbohidratos', 'grasas']:
                resultados[grupo][key] /= total_usuarios
            for nutriente in resultados[grupo]['nutrientes']:
                resultados[grupo]['nutrientes'][nutriente] /= total_usuarios

    return resultados

# Evalúa cuál grupo tiene un mayor riesgo basado en su consumo nutricional. Utiliza los resultados del análisis de consumo
# para comparar el consumo calórico y de macronutrientes entre los dos grupos, así como la diversidad de nutrientes consumidos.
# Proporciona como resultado un grupo con mayor riesgo y las razones de esta evaluación.
def evaluar_grupos(resultados):
    evaluacion = {
        'grupo_mas_riesgo': '',
        'razones': []
    }

    # Comparar consumo calórico
    if resultados['menores_30']['calorias'] > resultados['mayores_30']['calorias']:
        evaluacion['grupo_mas_riesgo'] = 'El grupo de menores de 30'
        evaluacion['razones'].append('mayor consumo calórico')
    else:
        evaluacion['grupo_mas_riesgo'] = 'El grupo de mayores de 30'
        evaluacion['razones'].append('mayor consumo calórico')

    # Comparar macronutrientes
    for nutriente in ['proteinas', 'carbohidratos', 'grasas']:
        if resultados['menores_30'][nutriente] > resultados['mayores_30'][nutriente]:
            evaluacion['razones'].append(f'mayor consumo de {nutriente} en menores de 30')
        else:
            evaluacion['razones'].append(f'mayor consumo de {nutriente} en mayores de 30')

    # Comparar diversidad de nutrientes
    nutrientes_menores_30 = set(resultados['menores_30']['nutrientes'].keys())
    nutrientes_mayores_30 = set(resultados['mayores_30']['nutrientes'].keys())
    if len(nutrientes_menores_30) < len(nutrientes_mayores_30):
        evaluacion['razones'].append('menor diversidad de nutrientes en menores de 30.')
    elif len(nutrientes_menores_30) > len(nutrientes_mayores_30):
        evaluacion['razones'].append('menor diversidad de nutrientes en mayores de 30.')

    return evaluacion

# Ejecutar análisis y evaluación
resultados_analisis = analisis_consumo()
evaluacion_final = evaluar_grupos(resultados_analisis)

# Realiza un análisis de consumo utilizando la función analisis_consumo, evalúa los grupos con evaluar_grupos,
# y prepara los datos para ser visualizados en gráficos. Finalmente, envía esos datos a un template HTML
# para su visualización. Es una vista de alto nivel que integra la lógica de análisis con la presentación de datos.
def vista_analisis(request):
    fecha_inicio = request.GET.get('fecha_inicio') # o como se envíe el parámetro
    fecha_fin = request.GET.get('fecha_fin') # o como se envíe el parámetro
    resultados_analisis = analisis_consumo(fecha_inicio, fecha_fin)
    evaluacion_final = evaluar_grupos(resultados_analisis)

    # Preparar datos para gráficos
    datos_graficos = {
        'menores_30': {
            'calorias': resultados_analisis['menores_30']['calorias'],
            'proteinas': resultados_analisis['menores_30']['proteinas'],
            'carbohidratos': resultados_analisis['menores_30']['carbohidratos'],
            'grasas': resultados_analisis['menores_30']['grasas'],
            'nutrientes': resultados_analisis['menores_30']['nutrientes']
        },
        'mayores_30': {
            'calorias': resultados_analisis['mayores_30']['calorias'],
            'proteinas': resultados_analisis['mayores_30']['proteinas'],
            'carbohidratos': resultados_analisis['mayores_30']['carbohidratos'],
            'grasas': resultados_analisis['mayores_30']['grasas'],
            'nutrientes': resultados_analisis['mayores_30']['nutrientes']
        }
    }

    context = {
        'evaluacion': evaluacion_final,
        'datos_graficos': datos_graficos
    }

    return render(request, 'analisis-consumo.html', context)


# Muestra la página principal de la aplicación (index.html). Es una vista simple que no realiza
# ninguna operación más allá de renderizar la página.
def main_page(request):
    return render(request, 'index.html')


# Realiza y muestra un análisis nutricional del usuario basado en su perfil nutricional y registros diarios.
# Calcula las necesidades nutricionales del usuario y compara su ingesta diaria con estas necesidades.
# Si el usuario ha cumplido sus límites nutricionales para el día, muestra un mensaje de felicitación.
def analisis_nutricional(request):
    perfil = get_object_or_404(PerfilNutricional, usuario=request.user)
    registros = RegistroDiario.objects.filter(usuario=request.user, fecha=date.today())
    necesidades = calcular_necesidades_nutricionales(perfil)
    analisis = analizar_ingesta_nutricional(registros, necesidades)

    if ha_cumplido_limites(analisis, necesidades):
        messages.success(request, '¡Felicidades! Has cumplido con tu dosis diaria.')

    return render(request, 'base/analisis_nutricional.html', {'analisis': analisis})

# Proporciona sugerencias nutricionales personalizadas a usuarios autenticados basándose en su perfil e ingesta diaria.
def sugerencias_alimentos(request):
    # Obtener el perfil nutricional del usuario
    perfil = get_object_or_404(PerfilNutricional, usuario=request.user)
    bmr = calcular_bmr(perfil)

    # Filtrar registros por la fecha de hoy
    registros = RegistroDiario.objects.filter(usuario=request.user, fecha=date.today())
    necesidades = calcular_necesidades_nutricionales(perfil)
    analisis = analizar_ingesta_nutricional(registros, necesidades)

    # Obtener top 5 de alimentos ricos en micronutrientes y macronutrientes
    sugerencias_macro_micro = Alimento.objects.filter(usuario=request.user).annotate(total_macro=F('proteinas') + F('carbohidratos') + F('grasas') + F('nutrientes')).order_by('-total_macro')[:5]

    Alimento.objects.filter(usuario=request.user)


    return render(request, 'base/sugerencias_alimentos.html', {
        'bmr': bmr,
        'analisis': analisis,
        'sugerencias_macro_micro': sugerencias_macro_micro,
    })




