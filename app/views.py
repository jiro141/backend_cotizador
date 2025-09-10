import os
import json
from datetime import timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .filters import RespuestaFilter
from .models import *
from .serializers import *
from .utils import generate_token1, generate_token2, send_reset_email


# ============================
# ViewSets de modelos principales
# ============================

class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer


class TipouserViewSet(viewsets.ModelViewSet):
    queryset = Tipouser.objects.all()
    serializer_class = TipouserSerializer


class PreguntasViewSet(viewsets.ModelViewSet):
    queryset = Preguntas.objects.all()
    serializer_class = PreguntasSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class ElementoPortadaViewSet(viewsets.ModelViewSet):
    queryset = ElementoPortada.objects.all()
    serializer_class = ElementoPortadaSerializer


class PaginaBasicaViewSet(viewsets.ModelViewSet):
    queryset = PaginaBasica.objects.all()
    serializer_class = PaginaBasicaSerializer


class FuncionAdicionalViewSet(viewsets.ModelViewSet):
    queryset = FuncionAdicional.objects.all()
    serializer_class = FuncionAdicionalSerializer


class MensualViewSet(viewsets.ModelViewSet):
    queryset = Mensual.objects.all()
    serializer_class = MensualSerializer


class RespuestaViewSet(viewsets.ModelViewSet):
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RespuestaFilter


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer


class BeneficioViewSet(viewsets.ModelViewSet):
    queryset = Beneficio.objects.all()
    serializer_class = BeneficioSerializer


class TipoBeneficioViewSet(viewsets.ModelViewSet):
    queryset = TipoBeneficio.objects.all()
    serializer_class = TipoBeneficioSerializer


class PuntajeBeneficioProductoViewSet(viewsets.ModelViewSet):
    queryset = PuntajeBeneficioProducto.objects.all()
    serializer_class = PuntajeBeneficioProductoSerializer


# ============================
# Autenticación y login
# ============================

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario no registrado."}, status=status.HTTP_400_BAD_REQUEST)

        # Usuario sin contraseña configurada
        if not user.password:
            if not password:
                return Response({"message": "Configure su contraseña"}, status=status.HTTP_200_OK)
            else:
                user.password = make_password(password)
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'email': user.email,
                }, status=status.HTTP_200_OK)

        # Validar contraseña
        if not check_password(password, user.password):
            return Response({"error": "Contraseña incorrecta."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'tipouser_id': user.tipoUser_id,
            'pais_id': user.pais_id,
        }, status=status.HTTP_200_OK)


# ============================
# Flujo de recuperación de contraseña
# ============================

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message": "Si el correo existe, recibirás instrucciones."}, status=status.HTTP_200_OK)

        PasswordResetToken.objects.filter(user=user, used=False).delete()

        token1 = generate_token1()
        expires_at = timezone.now() + timedelta(minutes=5)

        PasswordResetToken.objects.create(
            user=user,
            token1=token1,
            token1_expires_at=expires_at
        )

        send_reset_email(email, token1)
        return Response({"message": "Si el correo existe, recibirás instrucciones."}, status=status.HTTP_200_OK)


class PasswordResetVerifyView(APIView):
    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        token1 = serializer.validated_data['token1']

        try:
            user = CustomUser.objects.get(email=email)
            prt = PasswordResetToken.objects.get(user=user, token1=token1, used=False)
        except (CustomUser.DoesNotExist, PasswordResetToken.DoesNotExist):
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        if not prt.is_token1_valid():
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        token2 = generate_token2()
        token2_expires_at = timezone.now() + timedelta(minutes=5)

        prt.token2 = token2
        prt.token2_expires_at = token2_expires_at
        prt.save()

        return Response({"token2": token2}, status=status.HTTP_200_OK)


class PasswordResetChangeView(APIView):
    def post(self, request):
        serializer = PasswordResetChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        token2 = serializer.validated_data['token2']
        new_password = serializer.validated_data['new_password']

        try:
            user = CustomUser.objects.get(email=email)
            prt = PasswordResetToken.objects.get(user=user, token2=token2, used=False)
        except (CustomUser.DoesNotExist, PasswordResetToken.DoesNotExist):
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        if not prt.is_token2_valid():
            return Response({"error": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        prt.used = True
        prt.save()

        return Response({"message": "Contraseña cambiada correctamente."}, status=status.HTTP_200_OK)


# ============================
# Integración con Google Docs
# ============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOOGLE_CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents"
]


def authorize(request):
    """Redirige al login de Google para autorizar la app"""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8000/api/oauth2callback"
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return HttpResponseRedirect(auth_url)


def oauth2callback(request):
    """Callback de Google OAuth2: guarda el token de acceso"""
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8000/api/oauth2callback"
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    creds = flow.credentials
    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

    return JsonResponse({"status": "ok", "message": "Autenticado con Google 🚀"})


@csrf_exempt
def create_doc(request):
    """Crea un Google Doc en el Drive y lo guarda en BD"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    contenido = body.get("contenido")
    correo = body.get("correo")
    cliente = body.get("cliente")
    empresa = body.get("empresa")

    if not contenido or not correo or not cliente or not empresa:
        return JsonResponse({"error": "Faltan campos: contenido, correo, cliente o empresa"}, status=400)

    if not os.path.exists(TOKEN_FILE):
        return JsonResponse({"error": "Cuenta de Google no autenticada"}, status=401)

    try:
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        service_drive = build("drive", "v3", credentials=creds)
        service_docs = build("docs", "v1", credentials=creds)

        # Crear documento en Drive
        file_metadata = {
            "name": "Documento Django API",
            "mimeType": "application/vnd.google-apps.document"
        }
        file = service_drive.files().create(body=file_metadata, fields="id").execute()
        doc_id = file.get("id")

        # Insertar contenido
        service_docs.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": contenido}}]}
        ).execute()

        # Compartir documento con el correo indicado
        permission = {"type": "user", "role": "writer", "emailAddress": correo}
        service_drive.permissions().create(fileId=doc_id, body=permission).execute()

        # Guardar en base de datos
        documento = Documento.objects.create(
            document_id=doc_id,   # PK
            usuario=request.user,
            correo_compartido=correo,
            cliente=cliente,
            empresa=empresa,
            contenido=contenido,
            link=f"https://docs.google.com/document/d/{doc_id}/edit"
        )

        return JsonResponse({
            "status": "ok",
            "documentId": documento.document_id,
            "link": documento.link,
            "cliente": documento.cliente,
            "empresa": documento.empresa,
            "fecha_creacion": documento.fecha_creacion.isoformat()
        })

    except HttpError as e:
        if e.resp.status == 403 and "storageQuotaExceeded" in str(e):
            return JsonResponse(
                {"error": "La cuenta de Google Drive se quedó sin espacio de almacenamiento."},
                status=403
            )
        return JsonResponse({"error": f"Error de Google API: {e}"}, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all().order_by("-fecha_creacion")
    serializer_class = DocumentoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["cliente", "empresa", "usuario__name"]  # 🔎 búsqueda dinámica
    ordering_fields = ["fecha_creacion", "cliente", "empresa"]