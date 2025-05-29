# app/filters.py
import django_filters
from .models import Respuesta

class RespuestaFilter(django_filters.FilterSet):
    pregunta = django_filters.NumberFilter(field_name='pregunta__id')

    class Meta:
        model = Respuesta
        fields = ['pregunta']
