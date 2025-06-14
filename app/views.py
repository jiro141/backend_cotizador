from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import RespuestaFilter


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
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
