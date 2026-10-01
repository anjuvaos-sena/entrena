from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_autenticacion.urls')),
    path('convocatorias/', include('app_convocatorias.urls')),
    path('inscripciones/', include('app_inscripciones.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
