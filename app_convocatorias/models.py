from django.db import models
from django.core.exceptions import ValidationError


class Convocatoria(models.Model):
	class Estado(models.TextChoices):
		BORRADOR = 'Borrador', 'Borrador'
		PUBLICADA = 'Publicada', 'Publicada'
		CERRADA = 'Cerrada', 'Cerrada'
		CANCELADA = 'Cancelada', 'Cancelada'

	titulo = models.CharField(max_length=200)
	area = models.CharField(max_length=100)
	descripcion = models.TextField()
	fecha_inicio = models.DateField()
	fecha_final = models.DateField()
	ciudad = models.CharField(max_length=100)
	cupos_totales = models.PositiveIntegerField()
	cupos_asignados = models.PositiveIntegerField(default=0)
	estado = models.CharField(
		max_length=10,
		choices=Estado.choices,
		default=Estado.BORRADOR,
	)

	class Meta:
		ordering = ['fecha_inicio']

	def clean(self):
		errors = {}
		if self.fecha_final and self.fecha_inicio and self.fecha_final < self.fecha_inicio:
			errors['fecha_final'] = 'La fecha final no puede ser anterior a la fecha de inicio.'
		if self.cupos_asignados > self.cupos_totales:
			errors['cupos_asignados'] = 'Los cupos asignados no pueden superar los cupos totales.'
		if errors:
			raise ValidationError(errors)

	def __str__(self):
		return self.titulo
