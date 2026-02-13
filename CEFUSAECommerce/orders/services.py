from orders.models import Order, OrderItem
from orders.domain.builders import OrderBuilder
from orders.infra.factories import NotificationFactory, PaymentProcessorFactory


# Clase para gestionar las ordenes
class OrderService:
    
    # Inyeccion de dependencias
    # Se pueden pasar implementaciones concretas de notificador y procesador de pagos, o se crean por defecto usando las fábricas
    def __init__(self, notifier=None, payment_processor=None):
        if  notifier is None and NotificationFactory:
            self.notifier = NotificationFactory.create()
        else:
            self.notifier = notifier
        
        if payment_processor is None and PaymentProcessorFactory:
            self.payment_processor = PaymentProcessorFactory.create()
            
        else:
            self.payment_processor = payment_processor
            
    def create_order(self, customer_data, items, shipping_address, discount_code=None):
        """
        Creates a new order
        
        Args:
            customer_data (dict): {'name': str, 'email': str,...}
            items (list): [{'product_name': str, 'quantity': int, 'price': float}, ...]
            shipping_address (str): Delivery address
            discount_code (str, optional): Discount code like 'SAVE10'
        
        Returns:
            dict: {'success': bool, 'order_id': int/None, 'message': str}
        """
        
        try:
            
            # Validar customer
            if not customer_data or not customer_data.get('name') or not customer_data.get('email'):
                raise ValueError("Customer name and email are required")
            
            # Validar items
            if not items or len(items) == 0:
                raise ValueError("At least one item is required")
            
            # Validar shipping address
            if not shipping_address:
                raise ValueError("Shipping address is required")
            
            # Construir la orden usando el builder
            if OrderBuilder is None:
                return {
                    'success' : False,
                    'order_id' : None, 
                    'message': 'OrderBuilder not available.'
                }
                
            builder = OrderBuilder()
            builder.for_customer(customer_data)
            
            for item in items:
                builder.add_item(
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    price=item['price']
                    )
                
            builder.with_shipping_address(shipping_address)
            
            if discount_code:
                builder.with_discount(discount_code)
                
            order = builder.build()

            
            if self.notifier:
                try:
                    message = f"Your order #{order.id} has been created successfully. Total: ${order.total_amount}"
                    self.notifier.notify(
                        user_email=customer_data['email'],
                        message=message
                    )
                except Exception as e:
                    # Si falla el email, no se cancela la orden
                    print(f"Warning: Failed to send notification: {str(e)}")
        
            return {
                'success': True,
                'order_id': order.id,
                'total_amount': float(order.total_amount),
                'message': 'Order created successfully'
            }
        
        except ValueError as e:
            return {
                'success': False,
                'order_id': None,
                'message': str(e)
            }
        
        except Exception as e:
            return {
                'success': False,
                'order_id': None,
                'message': f'Error creating order: {str(e)}'
            }
                
            