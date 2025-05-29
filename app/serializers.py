from .models import Preguntas, Respuesta
from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class TipouserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipouser
        fields = '__all__'


class PreguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preguntas
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class ElementoPortadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementoPortada
        fields = '__all__'


class PaginaBasicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaginaBasica
        fields = '__all__'


class FuncionAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuncionAdicional
        fields = '__all__'


class MensualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensual
        fields = '__all__'
        from rest_framework import serializers


class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['pregunta', 'texto']


class PreguntaSerializer(serializers.ModelSerializer):
    respuesta = RespuestaSerializer(read_only=True)

    class Meta:
        model = Preguntas
        fields = ['id', 'pregunta', 'respuesta']


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'


class BeneficioSerializer(serializers.ModelSerializer):
    puntaje = serializers.SerializerMethodField()

    class Meta:
        model = Beneficio
        fields = ['id', 'name', 'descripcion', 'puntaje']

    def get_puntaje(self, obj):
        relaciones = PuntajeBeneficioProducto.objects.filter(beneficio=obj)
        return [
            {
                "producto_id": rel.producto.id,
                "puntaje": rel.puntaje
            } for rel in relaciones
        ]


class TipoBeneficioSerializer(serializers.ModelSerializer):
    beneficios = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Beneficio.objects.all()
    )

    class Meta:
        model = TipoBeneficio
        fields = ['id', 'nombre', 'descripcion', 'beneficios']


class PuntajeBeneficioProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntajeBeneficioProducto
        fields = '__all__'
