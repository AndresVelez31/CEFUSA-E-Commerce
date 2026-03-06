import random

# ─────────────────────────────────────────────────────────────────────────────
#  Payment Processors — Patrón Factory
#  Agregar una pasarela nueva: crear subclase de BasePaymentProcessor e
#  irla a registrar en PaymentProcessorFactory._registry.
# ─────────────────────────────────────────────────────────────────────────────


class BasePaymentProcessor:
    """
    Contrato base (LSP): cualquier subclase es intercambiable
    donde se espere un BasePaymentProcessor.
    """
    GATEWAY = 'base'

    def process_payment(self, amount: float) -> dict:
        raise NotImplementedError("Las subclases deben implementar process_payment()")


# ── Implementaciones ──────────────────────────────────────────────────────────

class MockPaymentProcessor(BasePaymentProcessor):
    """Desarrollo: simula el pago, no cobra nada real."""
    GATEWAY = 'mock'

    def process_payment(self, amount: float) -> dict:
        transaction_id = f"MOCK-{random.randint(100000, 999999)}"
        print(f"[MOCK PAYMENT] ${amount} | TxID: {transaction_id}")
        return {
            'success':        True,
            'transaction_id': transaction_id,
            'amount':         amount,
            'gateway':        self.GATEWAY,
            'message':        'Pago simulado (modo desarrollo)',
        }


class StripePaymentProcessor(BasePaymentProcessor):
    """Producción: integración con Stripe."""
    GATEWAY = 'stripe'

    def process_payment(self, amount: float) -> dict:
        # Aquí iría: import stripe; stripe.PaymentIntent.create(...)
        transaction_id = f"STRIPE-{random.randint(100000, 999999)}"
        print(f"[STRIPE] Procesando ${amount} | TxID: {transaction_id}")
        return {
            'success':        True,
            'transaction_id': transaction_id,
            'amount':         amount,
            'gateway':        self.GATEWAY,
            'message':        'Pago procesado via Stripe',
        }


class MercadoPagoPaymentProcessor(BasePaymentProcessor):
    """Alternativa: integración con MercadoPago."""
    GATEWAY = 'mercadopago'

    def process_payment(self, amount: float) -> dict:
        # Aquí iría: import mercadopago; sdk.payment().create(...)
        transaction_id = f"MP-{random.randint(100000, 999999)}"
        print(f"[MERCADOPAGO] Procesando ${amount} | TxID: {transaction_id}")
        return {
            'success':        True,
            'transaction_id': transaction_id,
            'amount':         amount,
            'gateway':        self.GATEWAY,
            'message':        'Pago procesado via MercadoPago',
        }


class PayPalPaymentProcessor(BasePaymentProcessor):
    """Alternativa: integración con PayPal."""
    GATEWAY = 'paypal'

    def process_payment(self, amount: float) -> dict:
        # Aquí iría la integración con PayPal REST API
        transaction_id = f"PP-{random.randint(100000, 999999)}"
        print(f"[PAYPAL] Procesando ${amount} | TxID: {transaction_id}")
        return {
            'success':        True,
            'transaction_id': transaction_id,
            'amount':         amount,
            'gateway':        self.GATEWAY,
            'message':        'Pago procesado via PayPal',
        }
