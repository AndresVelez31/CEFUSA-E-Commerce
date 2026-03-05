from rest_framework import serializers
from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer de lectura: expone todos los campos del cliente."""
    nombre_completo = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = ['id', 'nombre', 'apellido', 'nombre_completo',
                  'email', 'telefono', 'direccion', 'created_at']
        read_only_fields = ['id', 'created_at']


class CreateCustomerSerializer(serializers.ModelSerializer):
    """Serializer de escritura: valida la creación de un cliente."""

    class Meta:
        model = Customer
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion']

    def validate_email(self, value):
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Ya existe un cliente registrado con este email."
            )
        return value

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value.strip()

    def validate_apellido(self, value):
        if not value.strip():
            raise serializers.ValidationError("El apellido no puede estar vacío.")
        return value.strip()
