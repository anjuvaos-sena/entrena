# Reglas de desarrollo del proyecto

## 1. Arquitectura General
- El proyecto se desarrollará en **Django** bajo arquitectura estricta **MVT (Model–View–Template)**.
- Cada app será independiente y manejará sus propios `models.py`, `views.py`, `urls.py` y plantillas.  
- El `urls.py` del proyecto solo direccionará hacia las rutas de las apps.  
- El nombre de cada app debe iniciar con el prefijo `app_`.  
  - Ejemplo: `app_inscripciones`, `app_convocatorias`.  
- Las relaciones entre apps deben implementarse mediante `ForeignKey` o `ManyToMany` según corresponda, manteniendo trazabilidad entre convocatorias e inscripciones.

---

## 2. Estándares de Codificación
- Se seguirá estrictamente **PEP8**.  
- Convenciones de nombres:  
  - **Modelos**: PascalCase → `Convocatoria`, `Inscripcion`.  
  - **Variables, funciones y métodos**: snake_case → `validar_cupos()`, `fecha_inicio`.  
- Todos los archivos deben incluir docstrings normativos en clases y funciones.

---

## 3. Gestión de Usuarios, Grupos y Permisos
- La gestión de usuarios, grupos y permisos debe realizarse usando el modelo propio de Django (`django.contrib.auth`).  
- El acceso a las vistas se realizará con base en el GRUPO del usuario (**Administradores** o **Instructores**).  
- Solo el Superadmin podrá crear los grupos y asignar permisos.  
- Todas las vistas deben estar protegidas con `login_required` y, cuando aplique, `permission_required`.

---

## 4. Modelos y Base de Datos
- Los modelos deben ser creados en cada app.  
- Se debe usar el ORM de Django exclusivamente.  
- La base de datos en desarrollo será `db.sqlite3`.  
- En producción se permitirá migración a PostgreSQL, manteniendo compatibilidad ORM.  

---

## 5. URLs
- Todas las rutas deben seguir directrices de **arquitectura REST**:  
  - `/convocatorias/` → GET lista, POST crear.  
  - `/convocatorias/{id}/` → GET detalle, PUT actualizar, DELETE eliminar.  
- Cada ruta debe tener un alias (`name`) para ser referenciada en plantillas y vistas.  

---

## 6. Vistas
- Todas las vistas serán **FBV (Function-Based Views)**.  
- Los nombres de las funciones de vista deben llevar el sufijo `_view`.  
- Las vistas complejas deben dividirse en funciones auxiliares para mantener claridad.  
- Ejemplo: `inscripciones_create_view`, `inscripciones_list_view`.

---

## 7. Plantillas
- Las plantillas deben cumplir estrictamente con las directrices de **DESIGN.md**.  
- Se almacenarán en la carpeta `templates` dentro de cada app.  
- El nombre de cada plantilla debe iniciar con el nombre de la app.  
- Se utilizará **herencia de plantillas** con una plantilla base (`base.html`) que debe incluir:  
  - `{% block head %}`  
  - `{% block content %}`  
  - `{% block scripts %}`  
- Todas las plantillas deben ser **responsive**.

---

## 8. Archivos Estáticos
- Los archivos estáticos se organizarán en `static/` con subcarpetas por tipo (`css`, `js`, `img`).  
- Convenciones de nombres: `app_convocatorias.css`, `app_inscripciones.js`.  
- Se debe aplicar minificación y cache busting en producción.  

---

## 9. Dependencias y Librerías Externas
- Todas las dependencias deben declararse en `requirements.txt`.  
- Se permite **Bootstrap 5.x** únicamente para grid y utilidades.  
- No se permite modificar tipografía ni colores definidos en `DESIGN.md`.  

---

## 10. Seguridad y Buenas Prácticas
- Todas las entradas deben ser sanitizadas.  
- Se debe habilitar protección contra **CSRF** en formularios.  
- Contraseñas cifradas con algoritmos seguros (`PBKDF2`, `Argon2`).  
- Sesiones con expiración controlada y cookies seguras (`HttpOnly`, `Secure`).  
- Uso obligatorio de `django.middleware.security.SecurityMiddleware`.  
