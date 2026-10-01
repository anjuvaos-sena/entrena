from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from app_convocatorias.models import Convocatoria

from .models import Inscripcion


def _requiere_instructor(request):
	"""Verifica que el usuario autenticado pertenezca a Instructores."""
	if not request.user.groups.filter(name='Instructores').exists():
		raise PermissionDenied


def _datos_inscripcion(request):
	"""Obtiene y valida los datos personales enviados por el instructor."""
	datos = {
		'numero_identificacion': request.POST.get('numero_identificacion', '').strip(),
		'nombres': request.POST.get('nombres', '').strip(),
		'apellidos': request.POST.get('apellidos', '').strip(),
		'correo_electronico': request.POST.get('correo_electronico', '').strip(),
		'telefono': request.POST.get('telefono', '').strip(),
		'centro_formacion': request.POST.get('centro_formacion', '').strip(),
		'regional': request.POST.get('regional', '').strip(),
	}
	errores = {}
	for nombre, valor in datos.items():
		if not valor:
			errores[nombre] = 'Este campo es obligatorio.'

	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email(datos['correo_electronico'])
	except ValidationError:
		if datos['correo_electronico']:
			errores['correo_electronico'] = 'El correo electrónico no es válido.'

	archivo_pdf = request.FILES.get('archivo_pdf')
	if archivo_pdf is None:
		errores['archivo_pdf'] = 'Debe adjuntar un archivo PDF.'
	elif (
		not archivo_pdf.name.lower().endswith('.pdf')
		or archivo_pdf.content_type != 'application/pdf'
	):
		errores['archivo_pdf'] = 'Solo se aceptan archivos PDF.'

	return datos, archivo_pdf, errores


@login_required
def capacitaciones_publicadas_view(request):
	"""Muestra capacitaciones publicadas con filtros y búsqueda."""
	_requiere_instructor(request)
	convocatorias = Convocatoria.objects.filter(
		estado=Convocatoria.Estado.PUBLICADA,
	).annotate(cupos_disponibles=F('cupos_totales') - F('cupos_asignados'))
	area = request.GET.get('area', '').strip()
	ciudad = request.GET.get('ciudad', '').strip()
	busqueda = request.GET.get('q', '').strip()
	if area:
		convocatorias = convocatorias.filter(area=area)
	if ciudad:
		convocatorias = convocatorias.filter(ciudad=ciudad)
	if busqueda:
		convocatorias = convocatorias.filter(
			Q(titulo__icontains=busqueda)
			| Q(area__icontains=busqueda)
			| Q(descripcion__icontains=busqueda)
			| Q(ciudad__icontains=busqueda)
		)
	contexto = {
		'convocatorias': convocatorias,
		'areas': Convocatoria.objects.filter(
			estado=Convocatoria.Estado.PUBLICADA,
		).order_by('area').values_list('area', flat=True).distinct(),
		'ciudades': Convocatoria.objects.filter(
			estado=Convocatoria.Estado.PUBLICADA,
		).order_by('ciudad').values_list('ciudad', flat=True).distinct(),
		'area_seleccionada': area,
		'ciudad_seleccionada': ciudad,
		'busqueda': busqueda,
	}
	return render(
		request,
		'app_inscripciones/app_inscripciones_publicadas.html',
		contexto,
	)


@login_required
def crear_inscripcion_view(request, convocatoria_id):
	"""Registra una inscripción validando estado, año, cupos y PDF."""
	_requiere_instructor(request)
	convocatoria = get_object_or_404(Convocatoria, pk=convocatoria_id)
	if convocatoria.estado != Convocatoria.Estado.PUBLICADA:
		return redirect('app_inscripciones:capacitaciones_publicadas')
	datos = {}
	errores = {}
	if request.method == 'POST':
		datos, archivo_pdf, errores = _datos_inscripcion(request)
		if not errores:
			with transaction.atomic():
				convocatoria = Convocatoria.objects.select_for_update().get(
					pk=convocatoria_id,
				)
				if convocatoria.estado != Convocatoria.Estado.PUBLICADA:
					errores['convocatoria'] = 'La capacitación ya no está publicada.'
				elif convocatoria.cupos_asignados >= convocatoria.cupos_totales:
					errores['cupos'] = 'Los cupos de la capacitación están agotados.'
				elif Inscripcion.objects.filter(
					numero_identificacion=datos['numero_identificacion'],
					convocatoria__fecha_inicio__year=convocatoria.fecha_inicio.year,
				).exists():
					errores['anio'] = (
						'El instructor ya tiene una inscripción registrada en este año.'
					)
				else:
					Inscripcion.objects.create(
						convocatoria=convocatoria,
						numero_identificacion=datos['numero_identificacion'],
						nombres=datos['nombres'],
						apellidos=datos['apellidos'],
						correo_electronico=datos['correo_electronico'],
						telefono=datos['telefono'],
						centro_formacion=datos['centro_formacion'],
						regional=datos['regional'],
						archivo_pdf=archivo_pdf,
					)
					convocatoria.cupos_asignados += 1
					convocatoria.save(update_fields=['cupos_asignados'])
					return render(
						request,
						'app_inscripciones/app_inscripciones_form.html',
						{'convocatoria': convocatoria, 'confirmacion': True},
					)
	return render(
		request,
		'app_inscripciones/app_inscripciones_form.html',
		{'convocatoria': convocatoria, 'datos': datos, 'errores': errores},
	)
