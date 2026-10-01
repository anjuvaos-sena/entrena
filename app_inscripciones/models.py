from django.core.exceptions import ValidationError
from django.db import models


from app_convocatorias.models import Convocatoria


class Inscripcion(models.Model):
	"""Registra la inscripción de un instructor a una convocatoria."""

	convocatoria = models.ForeignKey(
		Convocatoria,
		on_delete=models.CASCADE,
		related_name='inscripciones',
	)
	numero_identificacion = models.CharField(max_length=30)
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	correo_electronico = models.EmailField(max_length=254)
	telefono = models.CharField(max_length=30)
	centro_formacion = models.CharField(max_length=150)
	regional = models.CharField(max_length=100)
	archivo_pdf = models.FileField(upload_to='requisitos_inscripciones/')
	fecha_inscripcion = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-fecha_inscripcion']

	def clean(self):
		"""Valida que el archivo asociado sea un PDF."""
		errores = {}
		if self.archivo_pdf:
			nombre = self.archivo_pdf.name.lower()
			tipo = getattr(self.archivo_pdf, 'content_type', '')
			if not nombre.endswith('.pdf') or tipo != 'application/pdf':
				errores['archivo_pdf'] = 'El archivo debe ser un PDF válido.'
		if errores:
			raise ValidationError(errores)

	def __str__(self):
		"""Devuelve una representación legible de la inscripción."""
		return f'{self.nombres} {self.apellidos} - {self.convocatoria}'
