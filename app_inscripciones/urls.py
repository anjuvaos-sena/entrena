from django.urls import path

from . import views


app_name = 'app_inscripciones'

urlpatterns = [
	path('', views.capacitaciones_publicadas_view, name='capacitaciones_publicadas'),
	path(
		'<int:convocatoria_id>/inscribirse/',
		views.crear_inscripcion_view,
		name='crear_inscripcion',
	),
]
