from django.conf import settings
from .notifiers import (
    BaseNotifier,
    MockNotifier, EmailNotifier, SMSNotifier, PushNotifier,
)
from .payment import (
    BasePaymentProcessor,
    MockPaymentProcessor, StripePaymentProcessor,
    MercadoPagoPaymentProcessor, PayPalPaymentProcessor,
)


class NotificationFactory:
    """
    Factory de notificadores con registro dinámico.

    El método activo se lee de settings.NOTIFICATION_METHOD.
    En modo desarrollo siempre se usa 'mock' salvo que se indique explícitamente.
    Se pueden registrar nuevos canales con NotificationFactory.register()
    sin modificar esta clase (OCP).
    """

    _registry: dict[str, type[BaseNotifier]] = {
        'mock':  MockNotifier,
        'email': EmailNotifier,
        'sms':   SMSNotifier,
        'push':  PushNotifier,
    }

    @classmethod
    def create(cls, method: str = None) -> BaseNotifier:
        """
        Instancia el notificador correspondiente.
        Prioridad: argumento explícito > settings.NOTIFICATION_METHOD > 'mock' en dev.
        """
        if method is None:
            method = (
                'mock'
                if settings.ENV_TYPE == 'development'
                else getattr(settings, 'NOTIFICATION_METHOD', 'email')
            )

        notifier_class = cls._registry.get(method)
        if notifier_class is None:
            available = list(cls._registry.keys())
            raise ValueError(
                f"Notificador '{method}' no registrado. "
                f"Opciones disponibles: {available}"
            )
        return notifier_class()

    @classmethod
    def register(cls, name: str, notifier_class: type[BaseNotifier]) -> None:
        """
        Registra un nuevo canal de notificación en tiempo de ejecución.
        Cumple OCP: extensión sin modificación.

        Uso:
            class WhatsAppNotifier(BaseNotifier): ...
            NotificationFactory.register('whatsapp', WhatsAppNotifier)
        """
        if not issubclass(notifier_class, BaseNotifier):
            raise TypeError(
                f"{notifier_class.__name__} debe heredar de BaseNotifier"
            )
        cls._registry[name] = notifier_class

    @classmethod
    def available_methods(cls) -> list[str]:
        """Retorna la lista de canales registrados."""
        return list(cls._registry.keys())


class PaymentProcessorFactory:
    """
    Factory de procesadores de pago con registro dinámico.

    La pasarela activa se lee de settings.PAYMENT_GATEWAY.
    En modo desarrollo siempre se usa 'mock'.
    Se pueden registrar nuevas pasarelas con PaymentProcessorFactory.register()
    sin modificar esta clase (OCP).
    """

    _registry: dict[str, type[BasePaymentProcessor]] = {
        'mock':        MockPaymentProcessor,
        'stripe':      StripePaymentProcessor,
        'mercadopago': MercadoPagoPaymentProcessor,
        'paypal':      PayPalPaymentProcessor,
    }

    @classmethod
    def create(cls, gateway: str = None) -> BasePaymentProcessor:
        """
        Instancia el procesador de pago correspondiente.
        Prioridad: argumento explícito > settings.PAYMENT_GATEWAY > 'mock' en dev.
        """
        if gateway is None:
            gateway = (
                'mock'
                if settings.ENV_TYPE == 'development'
                else getattr(settings, 'PAYMENT_GATEWAY', 'stripe')
            )

        processor_class = cls._registry.get(gateway)
        if processor_class is None:
            available = list(cls._registry.keys())
            raise ValueError(
                f"Pasarela '{gateway}' no registrada. "
                f"Opciones disponibles: {available}"
            )
        return processor_class()

    @classmethod
    def register(cls, name: str, processor_class: type[BasePaymentProcessor]) -> None:
        """
        Registra una nueva pasarela de pago en tiempo de ejecución.
        Cumple OCP: extensión sin modificación.

        Uso:
            class CulqiPaymentProcessor(BasePaymentProcessor): ...
            PaymentProcessorFactory.register('culqi', CulqiPaymentProcessor)
        """
        if not issubclass(processor_class, BasePaymentProcessor):
            raise TypeError(
                f"{processor_class.__name__} debe heredar de BasePaymentProcessor"
            )
        cls._registry[name] = processor_class

    @classmethod
    def available_gateways(cls) -> list[str]:
        """Retorna la lista de pasarelas registradas."""
        return list(cls._registry.keys())
