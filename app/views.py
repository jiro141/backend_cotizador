from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import RespuestaFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .utils import generate_token1, generate_token2, send_reset_email
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer


class TipouserViewSet(viewsets.ModelViewSet):
    queryset = Tipouser.objects.all()
    serializer_class = TipouserSerializer


class PreguntasViewSet(viewsets.ModelViewSet):
    queryset = Preguntas.objects.all()
    serializer_class = PreguntasSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class ElementoPortadaViewSet(viewsets.ModelViewSet):
    queryset = ElementoPortada.objects.all()
    serializer_class = ElementoPortadaSerializer


class PaginaBasicaViewSet(viewsets.ModelViewSet):
    queryset = PaginaBasica.objects.all()
    serializer_class = PaginaBasicaSerializer


class FuncionAdicionalViewSet(viewsets.ModelViewSet):
    queryset = FuncionAdicional.objects.all()
    serializer_class = FuncionAdicionalSerializer


class MensualViewSet(viewsets.ModelViewSet):
    queryset = Mensual.objects.all()
    serializer_class = MensualSerializer


class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Preguntas.objects.all()
    serializer_class = PreguntaSerializer


class RespuestaViewSet(viewsets.ModelViewSet):
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RespuestaFilter


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class BeneficioViewSet(viewsets.ModelViewSet):
    queryset = Beneficio.objects.all()
    serializer_class = BeneficioSerializer


class TipoBeneficioViewSet(viewsets.ModelViewSet):
    queryset = TipoBeneficio.objects.all()
    serializer_class = TipoBeneficioSerializer


class PuntajeBeneficioProductoViewSet(viewsets.ModelViewSet):
    queryset = PuntajeBeneficioProducto.objects.all()
    serializer_class = PuntajeBeneficioProductoSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario no registrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Si el usuario existe y la contraseña es vacía o None
        if not user.password:
            if not password:
                return Response({"message": "configure contraseña"}, status=status.HTTP_200_OK)
            else:
                user.password = password
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'email': user.email,
                }, status=status.HTTP_200_OK)
        else:
            if user.password != password:
                return Response({"error": "Contraseña incorrecta."}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'email': user.email,
                'tipouser_id': user.tipoUser_id,
                'pais_id': user.pais_id,
            }, status=status.HTTP_200_OK)


# Paso 1: Solicitar recuperación (envía token1)
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message": "Si el correo existe, recibirás instrucciones."}, status=status.HTTP_200_OK)
        # Elimina tokens antiguos no usados para el usuario
        PasswordResetToken.objects.filter(user=user, used=False).delete()
        token1 = generate_token1()
        expires_at = timezone.now() + timedelta(minutes=5)
        PasswordResetToken.objects.create(
            user=user,
            token1=token1,
            token1_expires_at=expires_at
        )
        send_reset_email(email, token1)
        return Response({"message": "Si el correo existe, recibirás instrucciones."}, status=status.HTTP_200_OK)

# Paso 2: Verificar token1 y recibir token2
class PasswordResetVerifyView(APIView):
    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        token1 = serializer.validated_data['token1']
        try:
            user = CustomUser.objects.get(email=email)
            prt = PasswordResetToken.objects.get(user=user, token1=token1, used=False)
        except (CustomUser.DoesNotExist, PasswordResetToken.DoesNotExist):
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)
        if not prt.is_token1_valid():
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)
        # Genera token2 y lo almacena
        token2 = generate_token2()
        token2_expires_at = timezone.now() + timedelta(minutes=5)
        prt.token2 = token2
        prt.token2_expires_at = token2_expires_at
        prt.save()
        return Response({"token2": token2}, status=status.HTTP_200_OK)

# Paso 3: Cambiar la contraseña con token2
class PasswordResetChangeView(APIView):
    def post(self, request):
        serializer = PasswordResetChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        token2 = serializer.validated_data['token2']
        new_password = serializer.validated_data['new_password']
        try:
            user = CustomUser.objects.get(email=email)
            prt = PasswordResetToken.objects.get(user=user, token2=token2, used=False)
        except (CustomUser.DoesNotExist, PasswordResetToken.DoesNotExist):
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)
        if not prt.is_token2_valid():
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)
        # Cambia la clave, hasheada con el sistema de Django
        user.password = make_password(new_password)
        user.save()
        prt.used = True
        prt.save()
        return Response({"message": "Contraseña cambiada correctamente."}, status=status.HTTP_200_OK)