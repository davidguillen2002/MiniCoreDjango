from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    main_page,
    vista_analisis,
)

urlpatterns = [
    path('', main_page, name='main_page'),
    path('analisis-consumo/', vista_analisis, name='analisis-consumo')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


