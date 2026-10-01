# Tutorial: archivos media en Django con Supabase S3

Guía básica para guardar archivos subidos por usuarios en un bucket de Supabase cuando la aplicación Django está desplegada en Render u otro hosting. El disco del servidor puede ser temporal; el bucket conserva los archivos aunque la aplicación se reinicie o vuelva a desplegar.

> Este ejemplo configura un bucket público. Úsalo solo para archivos que puedan ser consultados por cualquier persona con el enlace. Para documentos privados se necesita un bucket privado y URLs firmadas.

## 1. Crear el bucket y obtener las claves

En Supabase:

1. Crea un bucket de Storage y marca **Public bucket** si los archivos deben abrirse sin iniciar sesión.
2. En la configuración de Storage/S3 del proyecto, copia el endpoint S3, el Access Key y el Secret Key. Anota también el nombre exacto del bucket.
3. No confundas el endpoint S3 de carga con la URL pública de lectura. La aplicación usa el endpoint S3 para guardar; Django construye la URL pública para consultar.

No pongas las claves en el código, en este tutorial, ni en Git. Si una clave se publica por error, revócala y crea otra.

## 2. Instalar el backend S3

En la raíz del proyecto, instala y declara la dependencia:

```powershell
pip install "django-storages[s3]"
```

Agrega `django-storages[s3]` a `requirements.txt` y confirma que el proceso de build del hosting instala ese archivo:

```powershell
pip install -r requirements.txt
```

## 3. Configurar las variables de entorno

Agrega estas variables en la configuración del servicio web del hosting. En Render están en **Environment**. Usa los valores de tu propio proyecto Supabase, sin comillas:

| Variable | Valor |
| --- | --- |
| `SUPABASE_ACCESS_KEY` | Access Key S3 |
| `SUPABASE_SECRET_KEY` | Secret Key S3 |
| `SUPABASE_BUCKET` | Nombre del bucket |
| `SUPABASE_ENDPOINT` | Endpoint S3 completo, por ejemplo `https://<project-ref>.storage.supabase.co/storage/v1/s3` |
| `DEBUG` | `False` en producción |

Reinicia o vuelve a desplegar el servicio después de cambiar variables. Para desarrollo local, puedes dejar las variables sin definir y guardar archivos localmente; si tu proyecto usa un archivo `.env`, asegúrate de que esté en `.gitignore`.

## 4. Configurar Django

Este patrón usa `STORAGES`, disponible en Django 4.2 y posteriores. En `settings.py`, importa lo siguiente junto a los demás imports:

```python
import os
from urllib.parse import urlsplit
from django.core.exceptions import ImproperlyConfigured
```

Después de definir `DEBUG`, agrega la configuración. Si tu proyecto ya declara `STORAGES`, integra las dos entradas de este ejemplo en el diccionario existente; la entrada `staticfiles` es para archivos estáticos y no debe reemplazarse por el backend S3 de media.

```python
SUPABASE_ACCESS_KEY = os.environ.get("SUPABASE_ACCESS_KEY")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET")
SUPABASE_ENDPOINT = os.environ.get("SUPABASE_ENDPOINT")

supabase_values = [
    SUPABASE_ACCESS_KEY,
    SUPABASE_SECRET_KEY,
    SUPABASE_BUCKET,
    SUPABASE_ENDPOINT,
]
if any(supabase_values) and not all(supabase_values):
    raise ImproperlyConfigured("Define las cuatro variables SUPABASE.")

USE_SUPABASE_STORAGE = all(supabase_values)
if not DEBUG and not USE_SUPABASE_STORAGE:
    raise ImproperlyConfigured("Falta configurar el almacenamiento S3 en producción.")

STORAGES = {
    "default": {
        "BACKEND": (
            "storages.backends.s3.S3Storage"
            if USE_SUPABASE_STORAGE
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if not DEBUG
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

if USE_SUPABASE_STORAGE:
    endpoint_host = urlsplit(SUPABASE_ENDPOINT).hostname or ""
    suffix = ".storage.supabase.co"
    if not endpoint_host.endswith(suffix):
        raise ImproperlyConfigured("SUPABASE_ENDPOINT no tiene el hostname S3 esperado.")

    project_ref = endpoint_host[:-len(suffix)]
    public_domain = (
        f"{project_ref}.supabase.co/storage/v1/object/public/{SUPABASE_BUCKET}"
    )
    MEDIA_URL = f"https://{public_domain}/"

    AWS_ACCESS_KEY_ID = SUPABASE_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = SUPABASE_SECRET_KEY
    AWS_STORAGE_BUCKET_NAME = SUPABASE_BUCKET
    AWS_S3_ENDPOINT_URL = SUPABASE_ENDPOINT
    AWS_S3_REGION_NAME = "us-east-1"
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_CUSTOM_DOMAIN = public_domain
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = None
```

Si tu hosting no define `DEBUG=False` por defecto, configúralo explícitamente para producción. Si usas otro backend de archivos estáticos, conserva ese backend en `STORAGES["staticfiles"]`; Supabase en este ejemplo es únicamente para media.

## 5. Confirmar que el formulario recibe archivos

El modelo debe tener un `FileField` o `ImageField`. Define `upload_to` para ordenar los objetos dentro del bucket:

```python
archivo = models.FileField(upload_to="documentos/")
```

El formulario HTML debe permitir cargas y la vista debe pasar los archivos a Django:

```html
<form method="post" enctype="multipart/form-data">
```

```python
form = MiFormulario(request.POST, request.FILES)
```

Con un `ModelForm`, `form.save()` guarda el archivo a través del backend configurado. Para mostrarlo, usa `{{ objeto.archivo.url }}`; no construyas la URL concatenando rutas manualmente.

## 6. Desplegar y comprobar

1. Verifica en el hosting que existan las cuatro variables y que `DEBUG=False`.
2. Despliega la aplicación para instalar `requirements.txt` y cargar la configuración nueva. No hace falta una migración de base de datos solo por cambiar el backend de almacenamiento.
3. Ejecuta `python manage.py check` durante el build o localmente con la misma configuración de producción.
4. Sube un archivo pequeño desde la aplicación y abre su enlace. Una URL pública debe tener esta forma:

```text
https://<project-ref>.supabase.co/storage/v1/object/public/<bucket>/<carpeta>/<archivo>
```

5. Confirma que el archivo aparezca en el bucket. Si falla, revisa los logs del hosting y comprueba que las claves sean las credenciales S3, que el endpoint esté completo y que el bucket permita lectura pública.

Los archivos guardados antes en el disco local no se copian al bucket automáticamente. Si deben conservarse, súbelos manteniendo la misma ruta relativa que está guardada en la base de datos.
