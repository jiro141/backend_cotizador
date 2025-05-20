from django.urls import path, include
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

urlpatterns = [
    path('api/', include(router.urls)),
]
