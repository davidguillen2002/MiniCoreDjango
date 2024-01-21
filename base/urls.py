from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    main_page,
    vista_todos_alumnos,
)

urlpatterns = [
    path('', main_page, name='main_page'),
    path('resumen-alumnos/', vista_todos_alumnos, name='resumen-alumnos')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


