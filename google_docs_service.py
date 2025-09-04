from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "/home/detipcompany141/backend_cotizacion/credenciales.json"
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)
docs_service = build("docs", "v1", credentials=credentials)

def crear_doc_y_compartir(contenido: str, correo_destino: str):
    # Crear documento
    doc = docs_service.documents().create(body={"title": "Documento generado desde Django"}).execute()
    doc_id = doc.get("documentId")

    # Insertar texto recibido
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {"insertText": {"location": {"index": 1}, "text": contenido}}
            ]
        }
    ).execute()

    # Compartir con tu correo
    PERMISSION = {
        "type": "user",
        "role": "writer",
        "emailAddress": correo_destino
    }
    drive_service.permissions().create(fileId=doc_id, body=PERMISSION, fields="id").execute()

    return f"https://docs.google.com/document/d/{doc_id}/edit"
