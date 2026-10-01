from django.urls import path

from . import views


app_name = 'app_convocatorias'

urlpatterns = [
    path('', views.gestionar_convocatorias_view, name='gestionar_convocatorias'),
    path('admin-dashboard/', views.gestionar_convocatorias_view, name='admin_dashboard'),
    path('crear/', views.crear_convocatoria_view, name='crear_convocatoria'),
    path(
        '<int:convocatoria_id>/',
        views.convocatoria_detail_view,
        name='detalle_convocatoria',
    ),
    path(
        '<int:convocatoria_id>/estado/',
        views.cambiar_estado_convocatoria_view,
        name='cambiar_estado_convocatoria',
    ),
    path(
        '<int:convocatoria_id>/consulta/',
        views.consultar_convocatoria_view,
        name='consultar_convocatoria',
    ),
]