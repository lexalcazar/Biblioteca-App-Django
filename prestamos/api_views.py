
import rest_framework
from rest_framework import viewsets
from prestamos.models import Libro
from prestamos.serializers import LibroSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class Libros_api_view(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer


@api_view(['GET'])
def vista_por_titulo(request, titulo):
    libro = Libro.objects.filter(titulo__icontains=titulo).first()
    if libro:
        serializer = LibroSerializer(libro)
        return Response(serializer.data)
    return Response({'error': 'Libro no encontrado'}, status=404)

    