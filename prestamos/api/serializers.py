
from rest_framework import serializers

from prestamos.api.dni_utils import check_dni

# importamos el modelo usuario para poder usarlo en el serializer
from ..models import Usuario, Libro, Prestamo, Autor

#--------------------------------------
# serializer modelo autor
#--------------------------------------

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre']


#-------------------------------------
# serializer modelo libro
#-------------------------------------


class LibroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(many=True) # Incluimos el serializer de autor para mostrar los datos del autor en el libro
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor']

#-------------------------------------
# serializer para el detalle de un libro
#-------------------------------------


class DetalleLibroSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Libro
        fields = '__all__'


#-------------------------------------
# serializer modelo usuario
#-------------------------------------


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'dni', 'direccion', 'telefono', 'rol']


#-------------------------------------
# serializer para el detalle de un usuario
#-------------------------------------


class DetalleUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

#--------------------------------------------        
# serializer para crear un usuario
#----------------------------------------------

class CrearUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'dni',
            'direccion',
            'telefono',
            'rol',
            'password',
        ]
    # validamos el dni usando el mismo metodo que el endpoint de check_dni
    def validate_dni(self, value):

        validator = DNIValidatorSerializer(data={"documento": value}) # Creamos una instancia del serializer de validación de DNI con el valor a validar

        if not validator.is_valid():
            raise serializers.ValidationError(
                validator.errors["documento"][0] # Si el DNI no es válido, lanzamos una excepción con el error correspondiente
            )

        return value # Si el DNI es válido, devolvemos el valor sin modificar
    
    def create(self, validated_data): # Sobrescribimos el método create para crear un usuario con contraseña hasheada
        password = validated_data.pop('password')

        usuario = Usuario.objects.create_user(
            password=password,
            **validated_data
        )

        return usuario # Devolvemos el usuario creado
    
# ---------------------------------------------------------------
# serializer para validar el dni en el endpoint de check_dni
# ---------------------------------------------------------------


class DNIValidatorSerializer(serializers.Serializer):

    documento = serializers.CharField() # Campo para recibir el documento a validar

    def validate_documento(self, value): # Método de validación para el campo documento
        resultado = check_dni(value)

        if not resultado["valido"]: # Si el DNI no es válido, lanzamos una excepción con el error correspondiente
            raise serializers.ValidationError(resultado["error"])

        return value
    
#---------------------------------------------------------------
# serializer para el modelo prestamo
#---------------------------------------------------------------

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'
