from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsersViewSet, TipouserViewSet, PreguntasViewSet, ProductoViewSet,
    ElementoPortadaViewSet, PaginaBasicaViewSet, FuncionAdicionalViewSet,
    MensualViewSet, RespuestaViewSet, PaisViewSet, BeneficioViewSet,
    TipoBeneficioViewSet, PuntajeBeneficioProductoViewSet,
    LoginView, PasswordResetRequestView, PasswordResetVerifyView,
    PasswordResetChangeView, CrearDocumentoView
)

# ============================
# Router con todos los ViewSets
# ============================
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

# ============================
# URL patterns
# ============================
urlpatterns = [
    # Auth
    path('auth/login/', LoginView.as_view(), name='login'),

    # Password reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/verify/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
    path('password-reset/change/', PasswordResetChangeView.as_view(), name='password-reset-change'),

    # Google Docs
    path('crear-doc/', CrearDocumentoView.as_view(), name='crear-doc'),

    # Router con todos los modelos
    path('', include(router.urls)),
]
