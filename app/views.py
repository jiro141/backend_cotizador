from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import RespuestaFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
