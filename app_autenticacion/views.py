from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def login_view(request):
	"""Autentica al usuario y carga la plantilla de inicio de sesión."""
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		password = request.POST.get('password', '')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			if user.groups.filter(name='Administradores').exists():
				return redirect('app_convocatorias:gestionar_convocatorias')
			if user.groups.filter(name='Instructores').exists():
				return redirect('app_inscripciones:capacitaciones_publicadas')
			return redirect('login')

		return render(
			request,
			'app_autenticacion/login.html',
			{'error': 'El usuario o la contrasena no son validos.'},
		)

	return render(request, 'app_autenticacion/login.html')


def logout_view(request):
	"""Cierra la sesión actual y carga la plantilla de salida."""
	logout(request)
	return redirect('login')
