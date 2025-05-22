from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UsersViewSet,
    TipouserViewSet,
    PreguntasViewSet,  # ← uno solo
    ProductoViewSet,
    ElementoPortadaViewSet,
    PaginaBasicaViewSet,
    FuncionAdicionalViewSet,
    MensualViewSet,
    RespuestaViewSet,
)

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'tipousers', TipouserViewSet)
router.register(r'preguntas', PreguntasViewSet)  # solo uno
router.register(r'productos', ProductoViewSet)
router.register(r'elementos-portada', ElementoPortadaViewSet)
router.register(r'paginas-basicas', PaginaBasicaViewSet)
router.register(r'funciones', FuncionAdicionalViewSet)
router.register(r'mensuales', MensualViewSet)
router.register(r'respuestas', RespuestaViewSet)

urlpatterns = router.urls
