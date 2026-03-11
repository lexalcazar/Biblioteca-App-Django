
import rest_framework
from rest_framework import viewsets
from prestamos.models import Autor, Libro, Prestamo, Usuario
from prestamos.api.serializers import AutorSerializer, CrearUsuarioSerializer, DetalleLibroSerializer, DetalleUsuarioSerializer, LibroSerializer, PrestamoSerializer, UsuarioSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .dni_utils import check_dni
from rest_framework import generics

#-------------------------------------------------
# Vista para ver autores
#-----------------------------------------------------

class Autores_api_view(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

#----------------------------------------------------
# Vista para ver los prestamos
#-----------------------------------------------------

class Prestamos_api_view(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

#-----------------------------------------------------
# Vista para ver los libros
#-----------------------------------------------------


class Libros_api_view(viewsets.ModelViewSet):
    
    queryset = Libro.objects.all()
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetalleLibroSerializer
        return LibroSerializer
    


#---------------------------------------------
# vista para buscar un libro por su titulo
#---------------------------------------------


@api_view(['GET'])
def vista_por_titulo(request, titulo):
    libro = Libro.objects.filter(titulo__icontains=titulo).first()
    if libro:
        serializer = LibroSerializer(libro)
        return Response(serializer.data)
    return Response({'error': 'Libro no encontrado'}, status=404)


#---------------------------------------------
# vista para ver los usuarios
#---------------------------------------------

class Usuarios_api_view(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetalleUsuarioSerializer
        return UsuarioSerializer
    
#---------------------------------------------------    
# vista para crear un usuario
#-------------------------------------------------------


class CrearUsuarioAPIView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = CrearUsuarioSerializer


#-----------------------------------------------------------------
# endpoint para validar el dni
#-------------------------------------------------------------------


@api_view(['POST'])
def endpoint_check_dni(request):
    documento = request.data.get('documento')
    if not documento:
        return Response(
            {
                "error": "No se proporcionó el campo 'documento'"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    resultado = check_dni(documento)

    # DNI incorrecto
    if not resultado['valido']:
        return Response(
            resultado,
            status=status.HTTP_400_BAD_REQUEST,
            
        )

    # DNI correcto
    return Response(
        resultado,
        status=status.HTTP_200_OK
    
    )


    