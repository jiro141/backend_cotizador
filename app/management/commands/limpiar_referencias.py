from django.core.management.base import BaseCommand
from app.models import (
    CustomUser, Tipouser, Pais, Preguntas,
    GoogleToken, PasswordResetToken, Documento
)

class Command(BaseCommand):
    help = "Limpia referencias inválidas en FK y M2M para evitar errores de integridad."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Iniciando limpieza de referencias..."))

        # 1️⃣ Revisar usuarios y limpiar FK inválidas
        for user in CustomUser.objects.all():
            cambios = False

            if user.tipoUser_id and not Tipouser.objects.filter(id=user.tipoUser_id).exists():
                self.stdout.write(f" - Usuario {user.id}: FK tipoUser inválida -> NULL")
                user.tipoUser = None
                cambios = True

            if user.pais_id and not Pais.objects.filter(id=user.pais_id).exists():
                self.stdout.write(f" - Usuario {user.id}: FK pais inválida -> NULL")
                user.pais = None
                cambios = True

            if cambios:
                user.save()

        # 2️⃣ Revisar ManyToMany con Preguntas
        for user in CustomUser.objects.all():
            preguntas_ids = list(user.seguridad.values_list("id", flat=True))
            for pid in preguntas_ids:
                if not Preguntas.objects.filter(id=pid).exists():
                    self.stdout.write(f" - Usuario {user.id}: eliminando pregunta inválida {pid}")
                    user.seguridad.remove(pid)

        # 3️⃣ Revisar GoogleToken
        for token in GoogleToken.objects.all():
            if not CustomUser.objects.filter(id=token.user_id).exists():
                self.stdout.write(f" - GoogleToken {token.id}: user {token.user_id} inválido -> borrado")
                token.delete()

        # 4️⃣ Revisar PasswordResetToken
        for reset in PasswordResetToken.objects.all():
            if not CustomUser.objects.filter(id=reset.user_id).exists():
                self.stdout.write(f" - ResetToken {reset.id}: user {reset.user_id} inválido -> borrado")
                reset.delete()

        # 5️⃣ Revisar Documento
        for doc in Documento.objects.all():
            if not CustomUser.objects.filter(id=doc.usuario_id).exists():
                self.stdout.write(f" - Documento {doc.document_id}: usuario {doc.usuario_id} inválido -> borrado")
                doc.delete()

        self.stdout.write(self.style.SUCCESS("✅ Limpieza completada."))
