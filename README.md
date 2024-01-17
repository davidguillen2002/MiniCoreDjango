# Proyecto de Análisis Nutricional basado en Rango de Fechas (MINICORE)

Este proyecto Django se enfoca en el análisis del consumo nutricional de grupos de edades basándose en un rango de fechas específico. Calcula el promedio de consumo de calorías, grasas, proteínas, carbohidratos y nutrientes, proporcionando una visión clara y precisa del comportamiento alimentario de distintos grupos etarios.

## Características Principales

- **Filtrado por Rango de Fechas**: Permite seleccionar un rango de fechas específico para el análisis nutricional.
- **Análisis por Grupo de Edad**: Clasifica los datos según grupos de edad, ofreciendo insights especializados.
- **Cálculo de Promedios Nutricionales**: Calcula los promedios de consumo de calorías, grasas, proteínas, carbohidratos y nutrientes.
- **Visualización de Datos**: Presenta los resultados de manera gráfica para una fácil interpretación.

## Tecnologías Utilizadas

- Django
- Python
- HTML/CSS (para plantillas)
- Bibliotecas de visualización de datos (si corresponde)

## Estructura del Proyecto

### Modelos
Incluye modelos como `Alimento`, `PerfilNutricional`, `RegistroDiario`, `AlimentoNutriente`.

### Vistas
Contiene vistas clave como `analisis_consumo`, que es central para el proyecto, y otras como `main_page`, `analisis_nutricional`, `sugerencias_alimentos`.

### Utilidades
Funciones como `calcular_necesidades_nutricionales`, `analizar_ingesta_nutricional`, etc., que apoyan el análisis.

## Deploy en Render
El proyecto está desplegado en Render y puede ser accedido a través del siguiente enlace: 
https://minicore-jgre.onrender.com

## Cómo Instalar y Ejecutar

```bash
git clone https://github.com/davidguillen2002/MiniCoreDjango.git
cd [repositorio]
# Instalar dependencias
pip install -r requirements.txt
# Configurar y migrar la base de datos
python manage.py migrate
# Ejecutar el servidor
python manage.py runserver
