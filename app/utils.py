import random
from uuid import uuid4
from django.core.mail import send_mail


def generate_token1():
    # Genera un token de 6 dígitos numéricos para el correo
    return '{:06d}'.format(random.randint(0, 999999))


def generate_token2():
    # Genera un token seguro y largo para la segunda etapa
    return uuid4().hex


def send_reset_email(email, token1):
    reset_msg = f"Tu código de recuperación es: {token1}\nEste código expira en 5 minutos."
    send_mail(
        'Recupera tu contraseña',
        reset_msg,
        'info@detipcompany.com',   # <--- Remitente solicitado
        [email],
        fail_silently=False,
    )
