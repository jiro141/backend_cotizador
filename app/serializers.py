from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    CustomUser, Tipouser, Preguntas, Respuesta, Producto,
    ElementoPortada, PaginaBasica, FuncionAdicional, Mensual,
    Pais, Beneficio, TipoBeneficio, PuntajeBeneficioProducto,Documento
)


# ============================
# Serializers de modelos base
# ============================

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


# ============================
# Serializers para autenticación
# ============================

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, allow_blank=True, required=False, allow_null=True
    )

    def validate(self, data):
        email = data['email'].strip().lower()
        password = data.get('password', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Usuario no registrado.")

        # Si no tiene contraseña asignada
        if not user.password:
            if not password:
                raise serializers.ValidationError("configure contraseña")
            else:
                user.password = make_password(password)
                user.save()
        else:
            if not check_password(password, user.password):
                raise serializers.ValidationError("Contraseña incorrecta.")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'tipouser_id': user.tipoUser_id,
            'tipouser': user.tipoUser.nombre if user.tipoUser else None,
            'pais_id': user.pais_id,
            'pais': user.pais.nombre if user.pais else None,
        }


# ============================
# Serializers para reset de contraseña
# ============================

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    token1 = serializers.CharField()


class PasswordResetChangeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token2 = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


# ============================
# Serializer para Google Docs
# ============================

class DocumentoSerializer(serializers.Serializer):
    contenido = serializers.CharField()
    correo = serializers.EmailField()

class DocumentoSerializer(serializers.ModelSerializer):
    usuario_name = serializers.CharField(source="usuario.name", read_only=True)

    class Meta:
        model = Documento
        fields = [
            "document_id",
            "usuario",
            "usuario_name",
            "correo_compartido",
            "cliente",
            "empresa",
            "link",
            "fecha_creacion",
        ]