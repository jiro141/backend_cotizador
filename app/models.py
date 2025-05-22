from django.db import models


class Producto(models.Model):
    producto = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    valor = models.IntegerField()
    item = models.CharField(max_length=255, blank=True, null=True)

    paginas = models.ManyToManyField('PaginaBasica', blank=True)
    secciones = models.ManyToManyField('ElementoPortada', blank=True)
    funciones_obligatorias = models.ManyToManyField(
        'FuncionAdicional', blank=True)

    class Meta:
        db_table = 'producto'


class ElementoPortada(models.Model):
    seccion = models.CharField(max_length=255)
    valor = models.IntegerField()
    beneficio = models.CharField(max_length=255)
    productos = models.ManyToManyField(
        Producto, related_name="elementos", blank=True)

    class Meta:
        db_table = 'elemento_portada'


class FuncionAdicional(models.Model):
    pagina_avanzada = models.CharField(max_length=255)
    valor = models.IntegerField()
    productos = models.ManyToManyField(
        Producto, related_name="funciones_adicionales", blank=True)

    class Meta:
        db_table = 'funcion_adicional'


class PaginaBasica(models.Model):
    pagina = models.CharField(max_length=255)
    valor = models.IntegerField()
    productos = models.ManyToManyField(
        Producto, related_name="paginas_basicas", blank=True)

    class Meta:
        db_table = 'pagina_basica'


class Mensual(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valor = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'mensual'


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


class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    tipoUser = models.ForeignKey(
        Tipouser, on_delete=models.SET_NULL, null=True, blank=True)
    seguridad = models.ForeignKey(
        Preguntas, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'users'
