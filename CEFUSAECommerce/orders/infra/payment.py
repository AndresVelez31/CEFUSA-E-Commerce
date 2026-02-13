import random


class MockPaymentProcessor:
    
    def process_payment(self, amount: float) -> dict:
        transaction_id = f"MOCK-{random.randint(100000, 999999)}"
        
        print(f"[MOCK PAYMENT] Processing ${amount}")
        print(f"[MOCK PAYMENT] Transaction ID: {transaction_id}")
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'amount': amount,
            'processor': 'mock',
            'message': 'Payment simulated successfully (development mode)'
        }


class RealPaymentProcessor:
    
    def process_payment(self, amount: float) -> dict:
        print(f"[REAL PAYMENT] Processing ${amount} through payment gateway")
        
        transaction_id = f"REAL-{random.randint(100000, 999999)}"
        
        return {
            'success': True,
            'transaction_id': transaction_id,
            'amount': amount,
            'processor': 'real',
            'message': 'Payment processed successfully'
        }