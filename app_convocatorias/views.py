from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import QueryDict
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404, redirect, render

from .models import Convocatoria


def _requiere_administrador(request):
	"""Verifica que el usuario autenticado pertenezca a Administradores."""
	if not request.user.groups.filter(name='Administradores').exists():
		raise PermissionDenied


def _datos_convocatoria(request, datos_enviados=None):
	"""Obtiene y valida los datos enviados desde un formulario HTML."""
	datos_enviados = datos_enviados or request.POST
	errores = {}
	campos = {
		'titulo': datos_enviados.get('titulo', '').strip(),
		'area': datos_enviados.get('area', '').strip(),
		'descripcion': datos_enviados.get('descripcion', '').strip(),
		'fecha_inicio': datos_enviados.get('fecha_inicio', '').strip(),
		'fecha_final': datos_enviados.get('fecha_final', '').strip(),
		'ciudad': datos_enviados.get('ciudad', '').strip(),
		'cupos_totales': datos_enviados.get('cupos_totales', '').strip(),
	}

	for nombre, valor in campos.items():
		if not valor:
			errores[nombre] = 'Este campo es obligatorio.'

	fecha_inicio = parse_date(campos['fecha_inicio'])
	fecha_final = parse_date(campos['fecha_final'])
	if campos['fecha_inicio'] and fecha_inicio is None:
		errores['fecha_inicio'] = 'La fecha de inicio no es válida.'
	if campos['fecha_final'] and fecha_final is None:
		errores['fecha_final'] = 'La fecha final no es válida.'
	if fecha_inicio and fecha_final and fecha_final < fecha_inicio:
		errores['fecha_final'] = (
		'La fecha final no puede ser anterior a la fecha de inicio.'
	)

	cupos_totales = None
	if campos['cupos_totales']:
		try:
			cupos_totales = int(campos['cupos_totales'])
			if cupos_totales < 0:
				errores['cupos_totales'] = (
					'Los cupos totales deben ser mayores o iguales a cero.'
				)
		except ValueError:
			errores['cupos_totales'] = 'Los cupos totales deben ser un entero.'

	return campos, fecha_inicio, fecha_final, cupos_totales, errores


@login_required
def gestionar_convocatorias_view(request):
	"""Muestra todas las convocatorias con filtros y búsqueda administrativa."""
	_requiere_administrador(request)
	if request.method == 'POST':
		return _crear_convocatoria(request)

	convocatorias = Convocatoria.objects.all()
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
		'areas': Convocatoria.objects.order_by('area').values_list('area', flat=True).distinct(),
		'ciudades': Convocatoria.objects.order_by('ciudad').values_list('ciudad', flat=True).distinct(),
		'area_seleccionada': area,
		'ciudad_seleccionada': ciudad,
		'busqueda': busqueda,
	}
	return render(request, 'app_convocatorias/app_convocatorias_gestionar.html', contexto)


def _crear_convocatoria(request):
	"""Procesa el alta de una convocatoria desde un formulario HTML."""
	campos, fecha_inicio, fecha_final, cupos_totales, errores = _datos_convocatoria(request)
	if not errores:
		Convocatoria.objects.create(
			titulo=campos['titulo'],
			area=campos['area'],
			descripcion=campos['descripcion'],
			fecha_inicio=fecha_inicio,
			fecha_final=fecha_final,
			ciudad=campos['ciudad'],
			cupos_totales=cupos_totales,
			estado=Convocatoria.Estado.BORRADOR,
			cupos_asignados=0,
		)
		return redirect('app_convocatorias:gestionar_convocatorias')

	return render(
		request,
		'app_convocatorias/app_convocatorias_form.html',
		{'modo': 'Crear', 'datos': campos, 'errores': errores},
	)


@login_required
def crear_convocatoria_view(request):
	"""Crea una convocatoria nueva en estado Borrador."""
	_requiere_administrador(request)
	if request.method == 'POST':
		return _crear_convocatoria(request)

	return render(
		request,
		'app_convocatorias/app_convocatorias_form.html',
		{'modo': 'Crear', 'datos': {}, 'errores': {}},
	)


@login_required
def editar_convocatoria_view(request, convocatoria_id):
	"""Edita los datos permitidos de una convocatoria existente."""
	_requiere_administrador(request)
	convocatoria = get_object_or_404(Convocatoria, pk=convocatoria_id)
	datos = {
		'titulo': convocatoria.titulo,
		'area': convocatoria.area,
		'descripcion': convocatoria.descripcion,
		'fecha_inicio': convocatoria.fecha_inicio.isoformat(),
		'fecha_final': convocatoria.fecha_final.isoformat(),
		'ciudad': convocatoria.ciudad,
		'cupos_totales': convocatoria.cupos_totales,
	}
	if request.method in ('POST', 'PUT'):
		datos_enviados = request.POST
		if request.method == 'PUT':
			datos_enviados = QueryDict(request.body.decode('utf-8'))
		campos, fecha_inicio, fecha_final, cupos_totales, errores = _datos_convocatoria(
			request,
			datos_enviados,
		)
		if not errores and cupos_totales < convocatoria.cupos_asignados:
			errores['cupos_totales'] = (
				'Los cupos totales no pueden ser menores que los cupos asignados.'
			)
		datos = campos
		if not errores:
			for nombre in ('titulo', 'area', 'descripcion', 'ciudad'):
				setattr(convocatoria, nombre, campos[nombre])
			convocatoria.fecha_inicio = fecha_inicio
			convocatoria.fecha_final = fecha_final
			convocatoria.cupos_totales = cupos_totales
			convocatoria.full_clean()
			convocatoria.save()
			return redirect('app_convocatorias:gestionar_convocatorias')
	else:
		errores = {}

	return render(
		request,
		'app_convocatorias/app_convocatorias_form.html',
		{
			'datos': datos,
			'errores': errores,
			'modo': 'Editar',
			'convocatoria': convocatoria,
		},
	)


@login_required
def convocatoria_detail_view(request, convocatoria_id):
	"""Expone GET, actualización y eliminación REST de una convocatoria."""
	_requiere_administrador(request)
	convocatoria = get_object_or_404(Convocatoria, pk=convocatoria_id)
	if request.method == 'DELETE':
		convocatoria.delete()
		return redirect('app_convocatorias:gestionar_convocatorias')
	return editar_convocatoria_view(request, convocatoria_id)


@login_required
def cambiar_estado_convocatoria_view(request, convocatoria_id):
	"""Actualiza el estado de una convocatoria desde el dashboard."""
	_requiere_administrador(request)
	convocatoria = get_object_or_404(Convocatoria, pk=convocatoria_id)
	errores = {}
	if request.method == 'POST':
		estado = request.POST.get('estado', '')
		estados_validos = Convocatoria.Estado.values
		if estado not in estados_validos:
			errores['estado'] = 'El estado seleccionado no es válido.'
		else:
			convocatoria.estado = estado
			convocatoria.save(update_fields=['estado'])
			return redirect('app_convocatorias:gestionar_convocatorias')

	return render(
		request,
		'app_convocatorias/app_convocatorias_estado_form.html',
		{
			'convocatoria': convocatoria,
			'estados': Convocatoria.Estado.choices,
			'errores': errores,
		},
	)


@login_required
def consultar_convocatoria_view(request, convocatoria_id):
	"""Muestra las estadísticas y los instructores de una convocatoria."""
	_requiere_administrador(request)
	convocatoria = get_object_or_404(Convocatoria, pk=convocatoria_id)
	inscripciones = convocatoria.inscripciones.all()
	inscritos = inscripciones.count()
	porcentaje_inscripcion = 0
	if convocatoria.cupos_totales > 0:
		porcentaje_inscripcion = round(
			(inscritos / convocatoria.cupos_totales) * 100,
			2,
		)
	porcentaje_grafica = min(int(round(porcentaje_inscripcion)), 100)
	return render(
		request,
		'app_convocatorias/app_convocatorias_consultar.html',
		{
			'convocatoria': convocatoria,
			'inscripciones': inscripciones,
			'inscritos': inscritos,
			'porcentaje_inscripcion': porcentaje_inscripcion,
			'porcentaje_grafica': porcentaje_grafica,
		},
	)
