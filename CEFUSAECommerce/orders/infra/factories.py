from django.conf import settings
from .notifiers import MockNotifier, EmailNotifier
from .payment import MockPaymentProcessor, RealPaymentProcessor


class NotificationFactory:
    
    @staticmethod
    def create():
        if settings.ENV_TYPE == 'development':
            return MockNotifier()
        return EmailNotifier()


class PaymentProcessorFactory:
    
    @staticmethod
    def create():
        if settings.ENV_TYPE == 'development':
            return MockPaymentProcessor()
        return RealPaymentProcessor()
