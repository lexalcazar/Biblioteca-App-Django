
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from prestamos.api.api_views import Autores_api_view, CrearUsuarioAPIView, Libros_api_view, Prestamos_api_view, Usuarios_api_view, endpoint_check_dni, vista_por_titulo

# Crea el router y registra los ViewSets
router = DefaultRouter()
router.register(r'libros', Libros_api_view)   # Genera /api/libros/
router.register(r'usuarios', Usuarios_api_view)   # Genera /api/usuarios/
router.register(r'prestamos', Prestamos_api_view)   # Genera /api/prestamos/
router.register(r'autores', Autores_api_view)   # Genera /api/autores/


urlpatterns = [
    path('', include(router.urls)),
    path('libros/titulo/<str:titulo>/', vista_por_titulo),
    path('usuario/check_dni/', endpoint_check_dni),
    path('usuario/crear/', CrearUsuarioAPIView.as_view()),
]
