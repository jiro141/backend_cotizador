from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'tipousers', TipouserViewSet)
router.register(r'preguntas', PreguntasViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'elementos-portada', ElementoPortadaViewSet)
router.register(r'paginas-basicas', PaginaBasicaViewSet)
router.register(r'funciones', FuncionAdicionalViewSet)
router.register(r'mensuales', MensualViewSet)
router.register(r'respuestas', RespuestaViewSet)
router.register(r'paises', PaisViewSet)
router.register(r'beneficios', BeneficioViewSet)
router.register(r'tipo-beneficios', TipoBeneficioViewSet)
router.register(r'puntaje-beneficio-producto', PuntajeBeneficioProductoViewSet)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
]

# ✅ Importante: agregar rutas del router
urlpatterns += router.urls
