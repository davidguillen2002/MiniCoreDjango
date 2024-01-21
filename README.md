# Proyecto de Seguimiento Académico de Alumnos (MINICORE)

Este proyecto Django está diseñado para gestionar y analizar el rendimiento académico de los alumnos a lo largo de diferentes periodos de progreso. Permite calcular y visualizar las notas promedio de los alumnos en distintas fases del año académico, así como determinar las notas necesarias para alcanzar un objetivo de aprobación en fases futuras.

## Características Principales

- **Seguimiento de Progreso Académico**: Calcula las notas promedio de los alumnos en diferentes periodos.
- **Análisis por Alumno y Fecha**: Permite ver el rendimiento académico de cada alumno en rangos de fechas específicos.
- **Cálculo de Notas Necesarias**: Determina las notas que los alumnos necesitan obtener en futuros periodos para lograr un objetivo de aprobación.
- **Visualización de Datos**: Presenta los resultados de manera gráfica para facilitar la interpretación y el seguimiento.

## Tecnologías Utilizadas

- Django
- Python
- HTML/CSS (para plantillas)
- Bibliotecas de visualización de datos (si corresponde)

## Estructura del Proyecto

### Modelos

Incluye modelos como `Alumno`, `Nota`.

### Vistas

Contiene vistas clave como `vista_todos_alumnos`, que es central para el análisis del rendimiento académico, además de `main_page`.

### URLs

Definición de las rutas URL para acceder a las distintas vistas y funcionalidades del sistema.

### Administración

Configuración del sitio de administración de Django para gestionar las entidades `Nota` y `Alumno`.

## Cómo Instalar y Ejecutar

```bash
git clone https://github.com/davidguillen2002/MiniCoreDjango.git
cd [directorio del repositorio]
# Instalar dependencias
pip install -r requirements.txt
# Configurar y migrar la base de datos
python manage.py migrate
# Ejecutar el servidor
python manage.py runserver
