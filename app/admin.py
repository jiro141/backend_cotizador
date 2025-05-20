from django.contrib import admin
from .models import (
    Users,
    Tipouser,
    Preguntas,
    Producto,
    ElementoPortada,
    PaginaBasica,
    FuncionAdicional,
    Mensual
)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'tipoUser', 'seguridad')
    search_fields = ('name', 'email')


@admin.register(Tipouser)
class TipouserAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Preguntas)
class PreguntasAdmin(admin.ModelAdmin):
    list_display = ('pregunta',)
    search_fields = ('pregunta',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'valor', 'item')
    search_fields = ('producto',)
    filter_horizontal = ('paginas', 'secciones', 'funciones_obligatorias')


@admin.register(ElementoPortada)
class ElementoPortadaAdmin(admin.ModelAdmin):
    list_display = ('seccion', 'valor', 'beneficio')
    search_fields = ('seccion',)
    filter_horizontal = ('productos',)


@admin.register(PaginaBasica)
class PaginaBasicaAdmin(admin.ModelAdmin):
    list_display = ('pagina', 'valor')
    search_fields = ('pagina',)
    filter_horizontal = ('productos',)


@admin.register(FuncionAdicional)
class FuncionAdicionalAdmin(admin.ModelAdmin):
    list_display = ('pagina_avanzada', 'valor')
    search_fields = ('pagina_avanzada',)
    filter_horizontal = ('productos',)


@admin.register(Mensual)
class MensualAdmin(admin.ModelAdmin):
    list_display = ('producto', 'valor', 'precio')
    search_fields = ('producto__producto',)
