import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Scopes necesarios
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")


def get_credentials():
    """Obtiene o refresca las credenciales de Google"""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # ⚠️ Esto abre navegador la primera vez para dar permisos
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        # Guardamos el token para reutilizarlo en futuras peticiones
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return creds


def crear_doc_y_compartir(contenido: str, correo: str) -> str:
    """Crea un documento de Google Docs con contenido y lo comparte con un correo"""
    creds = get_credentials()

    # Crear servicios de Docs y Drive
    docs_service = build("docs", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    # Crear documento vacío
    doc = docs_service.documents().create(body={"title": "Documento API Django"}).execute()
    document_id = doc.get("documentId")

    # Insertar contenido en el documento
    requests = [
        {"insertText": {"location": {"index": 1}, "text": contenido}}
    ]
    docs_service.documents().batchUpdate(
        documentId=document_id, body={"requests": requests}
    ).execute()

    # Compartir el documento con el correo
    permission = {
        "type": "user",
        "role": "writer",
        "emailAddress": correo
    }
    drive_service.permissions().create(
        fileId=document_id,
        body=permission,
        fields="id"
    ).execute()

    # Retornar link del documento
    return f"https://docs.google.com/document/d/{document_id}/edit"