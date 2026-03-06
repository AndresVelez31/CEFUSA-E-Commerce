# ─────────────────────────────────────────────────────────────────────────────
#  Notifiers — Patrón Factory
#  Agregar un nuevo canal: crear una subclase de BaseNotifier e irla a
#  registrar en NotificationFactory._registry (no hay que tocar nada más).
# ─────────────────────────────────────────────────────────────────────────────


class BaseNotifier:
    """
    Contrato base (LSP): cualquier subclase es intercambiable
    donde se espere un BaseNotifier.
    """
    METHOD = 'base'

    def notify(self, user_email: str, message: str) -> dict:
        raise NotImplementedError("Las subclases deben implementar notify()")


# ── Implementaciones ──────────────────────────────────────────────────────────

class MockNotifier(BaseNotifier):
    """Desarrollo: imprime en consola, no envía nada real."""
    METHOD = 'mock'

    def notify(self, user_email: str, message: str) -> dict:
        print(f"[MOCK] To: {user_email} | {message}")
        return {
            'success':   True,
            'method':    self.METHOD,
            'recipient': user_email,
            'message':   'Notificación simulada (modo desarrollo)',
        }


class EmailNotifier(BaseNotifier):
    """Producción: envío real de correo electrónico."""
    METHOD = 'email'

    def notify(self, user_email: str, message: str) -> dict:
        # Aquí iría la integración con SendGrid / SES / SMTP
        print(f"[EMAIL] Enviando a: {user_email} | {message}")
        return {
            'success':   True,
            'method':    self.METHOD,
            'recipient': user_email,
            'message':   'Correo enviado exitosamente',
        }


class SMSNotifier(BaseNotifier):
    """Alternativa: notificación por SMS (ej. Twilio)."""
    METHOD = 'sms'

    def notify(self, user_email: str, message: str) -> dict:
        # user_email puede ser el teléfono o el identificador del usuario
        # Aquí iría la integración con Twilio / AWS SNS
        phone = user_email  # en este canal el campo actúa como teléfono
        print(f"[SMS] Enviando a: {phone} | {message}")
        return {
            'success':   True,
            'method':    self.METHOD,
            'recipient': phone,
            'message':   'SMS enviado exitosamente',
        }


class PushNotifier(BaseNotifier):
    """Alternativa: notificación push (ej. Firebase FCM)."""
    METHOD = 'push'

    def notify(self, user_email: str, message: str) -> dict:
        # Aquí iría la integración con Firebase Cloud Messaging
        print(f"[PUSH] Enviando push a token de: {user_email} | {message}")
        return {
            'success':   True,
            'method':    self.METHOD,
            'recipient': user_email,
            'message':   'Notificación push enviada exitosamente',
        }

