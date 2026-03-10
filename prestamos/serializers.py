
from rest_framework import serializers

# importamos el modelo usuario para poder usarlo en el serializer
from .models import Usuario, Libro, Prestamo, Autor




class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
        

