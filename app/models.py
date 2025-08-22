from django.db import models
from django.utils import timezone
from uuid import uuid4

class Producto(models.Model):
    producto = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    valor = models.IntegerField()
    item = models.CharField(max_length=255, blank=True, null=True)

    maxSecciones = models.IntegerField(default=0)
    maxPaginas = models.IntegerField(default=0)

    paginas = models.ManyToManyField('PaginaBasica', blank=True)
    secciones = models.ManyToManyField('ElementoPortada', blank=True)
    funciones_obligatorias = models.ManyToManyField(
        'FuncionAdicional', blank=True)

    def __str__(self):
        return self.producto

    class Meta:
        db_table = 'producto'


class ElementoPortada(models.Model):
    seccion = models.CharField(max_length=255)
    valor = models.IntegerField()
    beneficio = models.CharField(max_length=255)
    productos = models.ManyToManyField(
        Producto, related_name="elementos", blank=True)

    def __str__(self):
        return self.seccion  # O puedes usar self.beneficio si es más descriptivo

    class Meta:
        db_table = 'elemento_portada'


class FuncionAdicional(models.Model):
    pagina_avanzada = models.CharField(max_length=255)
    valor = models.IntegerField()
    productos = models.ManyToManyField(
        Producto, related_name="funciones_adicionales", blank=True)

    def __str__(self):
        return self.pagina_avanzada

    class Meta:
        db_table = 'funcion_adicional'


class PaginaBasica(models.Model):
    pagina = models.CharField(max_length=255)
    valor = models.IntegerField()
    productos = models.ManyToManyField(
        Producto, related_name="paginas_basicas", blank=True)

    def __str__(self):
        return self.pagina

    class Meta:
        db_table = 'pagina_basica'


class Mensual(models.Model):
    producto = models.CharField(max_length=255)  # ← Ya no es ForeignKey
    valor = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'mensual'

    def __str__(self):
        return f"{self.producto} (${self.precio})"




class Tipouser(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'tipouser'


class Preguntas(models.Model):
    pregunta = models.CharField(max_length=255)

    def __str__(self):
        return self.pregunta

    class Meta:
        db_table = 'preguntas'


class Respuesta(models.Model):
    pregunta = models.OneToOneField(
        Preguntas, on_delete=models.CASCADE, related_name='respuesta')
    texto = models.CharField(max_length=255)

    def __str__(self):
        return f"Respuesta a: {self.pregunta}"

    class Meta:
        db_table = 'respuestas'


class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    hora_trabajo = models.CharField(max_length=50, blank=True, null=True)
    clasificacion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'pais'

    def __str__(self):
        return self.nombre


class CustomUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)

    tipoUser = models.ForeignKey(
        Tipouser, on_delete=models.SET_NULL, null=True, blank=True
    )

    seguridad = models.ManyToManyField(
        Preguntas, blank=True, related_name='usuarios'
    )
    pais = models.ForeignKey(
        Pais, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'users'


class Beneficio(models.Model):
    name = models.CharField(max_length=100)
    descripcion = models.TextField()
    elementos_portada = models.ManyToManyField('ElementoPortada', related_name='beneficios', blank=True)
    funciones_adicionales = models.ManyToManyField('FuncionAdicional', related_name='beneficios', blank=True)
    paginas_basicas = models.ManyToManyField('PaginaBasica', related_name='beneficios', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'beneficios'



class TipoBeneficio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    beneficios = models.ManyToManyField('Beneficio', related_name='tipos')

    def __str__(self):
        return self.nombre


class PuntajeBeneficioProducto(models.Model):
    beneficio = models.ForeignKey('Beneficio', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    categoria = models.CharField(max_length=100)  # Ej: "Blog", "eCommerce"
    puntaje = models.PositiveIntegerField()  # Entre 0 y 100

    class Meta:
        unique_together = ('beneficio', 'producto', 'categoria')
        db_table = 'puntaje_beneficio_producto'
        verbose_name = 'Puntaje de Beneficio por Producto'
        verbose_name_plural = 'Puntajes de Beneficios por Producto'

    def __str__(self):
        producto_nombre = getattr(
            self.producto, 'producto', str(self.producto))
        beneficio_nombre = getattr(self.beneficio, 'name', str(self.beneficio))
        return f"{producto_nombre} - {self.categoria} ({beneficio_nombre}): {self.puntaje}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    token1 = models.CharField(max_length=64)
    token2 = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token1_expires_at = models.DateTimeField()
    token2_expires_at = models.DateTimeField(null=True, blank=True)
    used = models.BooleanField(default=False)

    def is_token1_valid(self):
        return not self.used and self.token1_expires_at > timezone.now()

    def is_token2_valid(self):
        return (
            not self.used and
            self.token2 and
            self.token2_expires_at and
            self.token2_expires_at > timezone.now()
        )
