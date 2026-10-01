from django.contrib import admin

from .models import Convocatoria


@admin.register(Convocatoria)
class ConvocatoriaAdmin(admin.ModelAdmin):
	list_display = (
		'titulo',
		'area',
		'fecha_inicio',
		'fecha_final',
		'ciudad',
		'cupos_totales',
		'cupos_asignados',
		'estado',
	)
	list_filter = ('area', 'ciudad', 'estado')
	search_fields = ('titulo', 'area', 'descripcion', 'ciudad')
