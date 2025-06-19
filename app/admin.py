from django.contrib import admin
from .models import (
    CustomUser,
    Tipouser,
    Preguntas,
    Producto,
    ElementoPortada,
    PaginaBasica,
    FuncionAdicional,
    Mensual,
    Pais,
    Beneficio, TipoBeneficio, PuntajeBeneficioProducto
)


@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'get_pais', 'get_preguntas')
    filter_horizontal = ('seguridad',)

    def get_preguntas(self, obj):
        return ", ".join([p.pregunta for p in obj.seguridad.all()])
    get_preguntas.short_description = 'Preguntas de seguridad'

    def get_pais(self, obj):
        return obj.pais.nombre if obj.pais else '—'
    get_pais.short_description = 'País'


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


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'hora_trabajo', 'clasificacion')
    search_fields = ('nombre', 'clasificacion')


@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descripcion')


@admin.register(TipoBeneficio)
class TipoBeneficioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    filter_horizontal = ('beneficios',)


@admin.register(PuntajeBeneficioProducto)
class PuntajeBeneficioProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'beneficio', 'categoria', 'puntaje')
    list_filter = ('categoria', 'producto', 'beneficio')
    search_fields = ('categoria', 'producto__name', 'beneficio__name')
