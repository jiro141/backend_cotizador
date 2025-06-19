from .models import Preguntas, Respuesta
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth.hashers import make_password, check_password

User = CustomUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
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


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, allow_blank=True, required=False, allow_null=True)

    def validate(self, data):
        email = data['email'].strip().lower()
        password = data.get('password', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Usuario no registrado.")

        if not user.password:
            if not password:
                raise serializers.ValidationError("configure contraseña")
            else:
                # Guardar la contraseña hasheada
                user.password = make_password(password)
                user.save()
        else:
            # Validar contraseña usando check_password
            if not check_password(password, user.password):
                raise serializers.ValidationError("Contraseña incorrecta.")

        # El campo is_active no existe en tu modelo. Si lo necesitas, agrégalo.
        # if not user.is_active:
        #     raise serializers.ValidationError("Cuenta inactiva.")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'tipouser': user.tipouser,
        }
