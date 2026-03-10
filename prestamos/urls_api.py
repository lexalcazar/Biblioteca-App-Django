
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from prestamos.api_views import Libros_api_view, vista_por_titulo

# Crea el router y registra los ViewSets
router = DefaultRouter()
router.register(r'libros', Libros_api_view)   # Genera /api/libros/

urlpatterns = [
    path('', include(router.urls)),
    path('libros/titulo/<str:titulo>/', vista_por_titulo),
]
