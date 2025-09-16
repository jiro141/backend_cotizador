from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import transaction, IntegrityError
from django.utils.translation import gettext_lazy as _

from .models import (
    CustomUser, Tipouser, Preguntas, Producto, ElementoPortada, PaginaBasica,
    FuncionAdicional, Mensual, Pais, Beneficio, TipoBeneficio,
    PuntajeBeneficioProducto, Documento, GoogleToken, PasswordResetToken, 
)

# =====================
# 🔹 Formularios de usuario
# =====================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "name", "tipoUser", "pais")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        pais = cleaned_data.get("pais")
        tipoUser = cleaned_data.get("tipoUser")

        if pais and not Pais.objects.filter(id=pais.id).exists():
            raise forms.ValidationError({"pais": "⚠️ El país seleccionado no existe."})

        if tipoUser and not Tipouser.objects.filter(id=tipoUser.id).exists():
            raise forms.ValidationError({"tipoUser": "⚠️ El tipo de usuario seleccionado no existe."})

        return cleaned_data


# =====================
# 🔹 Inlines relacionados
# =====================
class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 0


class GoogleTokenInline(admin.StackedInline):
    model = GoogleToken
    extra = 0


class PasswordResetTokenInline(admin.TabularInline):
    model = PasswordResetToken
    extra = 0


# =====================
# 🔹 Admin de CustomUser
# =====================
@admin.register(CustomUser)
class UsersAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ("id", "name", "email", "get_pais", "get_tipoUser", "get_preguntas", "is_active", "is_staff")
    list_filter = ("pais", "tipoUser", "is_active", "is_staff")
    search_fields = ("email", "name")
    ordering = ("id",)
    filter_horizontal = ("seguridad",)

    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        (_("Permisos"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Fechas"), {"fields": ("date_joined",)}),
        (_("Relaciones"), {"fields": ("tipoUser", "pais", "seguridad")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "tipoUser", "pais", "is_active", "is_staff", "is_superuser"),
        }),
    )

    inlines = [DocumentoInline, GoogleTokenInline, PasswordResetTokenInline]

    # 👇 Evita que el admin explote con integridad al guardar inlines/M2M
    def save_related(self, request, form, formsets, change):
        try:
            with transaction.atomic():
                super().save_related(request, form, formsets, change)
        except IntegrityError:
            self.message_user(
                request,
                "⚠️ Algunas relaciones inválidas fueron ignoradas al guardar este usuario.",
                level="warning"
            )

    # Helpers para mostrar datos relacionados
    def get_preguntas(self, obj):
        return ", ".join([p.pregunta for p in obj.seguridad.all()])
    get_preguntas.short_description = "Preguntas de seguridad"

    def get_pais(self, obj):
        return obj.pais.nombre if obj.pais else "—"
    get_pais.short_description = "País"

    def get_tipoUser(self, obj):
        return obj.tipoUser.name if obj.tipoUser else "—"
    get_tipoUser.short_description = "Tipo de usuario"


# =====================
# 🔹 Resto de modelos
# =====================
@admin.register(Tipouser)
class TipouserAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Preguntas)
class PreguntasAdmin(admin.ModelAdmin):
    list_display = ("id", "pregunta")
    search_fields = ("pregunta",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "valor", "item")
    search_fields = ("producto",)
    filter_horizontal = ("paginas", "secciones", "funciones_obligatorias")


@admin.register(ElementoPortada)
class ElementoPortadaAdmin(admin.ModelAdmin):
    list_display = ("id", "seccion", "valor", "beneficio")
    search_fields = ("seccion",)
    filter_horizontal = ("productos",)


@admin.register(PaginaBasica)
class PaginaBasicaAdmin(admin.ModelAdmin):
    list_display = ("id", "pagina", "valor")
    search_fields = ("pagina",)
    filter_horizontal = ("productos",)


@admin.register(FuncionAdicional)
class FuncionAdicionalAdmin(admin.ModelAdmin):
    list_display = ("id", "pagina_avanzada", "valor")
    search_fields = ("pagina_avanzada",)
    filter_horizontal = ("productos",)


@admin.register(Mensual)
class MensualAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "valor", "precio")
    search_fields = ("producto",)


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "hora_trabajo", "clasificacion")
    search_fields = ("nombre", "clasificacion")


@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "descripcion")


@admin.register(TipoBeneficio)
class TipoBeneficioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    filter_horizontal = ("beneficios",)


@admin.register(PuntajeBeneficioProducto)
class PuntajeBeneficioProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "beneficio", "categoria", "puntaje")
    list_filter = ("categoria", "producto", "beneficio")
    search_fields = ("categoria", "producto__producto", "beneficio__name")
    
    
@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ( "cliente", "empresa", "usuario", "monto", "fecha_creacion","link")
    search_fields = ("cliente", "empresa", "correo_compartido")
    list_filter = ("empresa", "fecha_creacion")
    ordering = ("-fecha_creacion",)