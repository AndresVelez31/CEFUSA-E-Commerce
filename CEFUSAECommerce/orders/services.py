try:
    from orders.models import Order, OrderItem
    from orders.domain.builders import OrderBuilder
    from orders.infra.factories import NotificationFactory, PaymentProcessorFactory
except ImportError:
    # Stubs temporales para que puedas trabajar sin esperar a tus compañeros
    OrderBuilder = None
    NotificationFactory = None
    PaymentProcessorFactory = None

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
            customer_data (dict): {'name': str, 'email': str, 'phone': str}
            items (list): [{'product_name': str, 'quantity': int, 'unit_price': float}, ...]
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
                    unit_price=item['unit_price']
                )
                
            builder.with_shipping_address(shipping_address)
            
            if discount_code:
                builder.with_discount(discount_code)
                
            order_data = builder.build()
            
            # Guardar en la base de datos
            order = Order.objects.create(
                customer_name=order_data['customer_name'],
                customer_email=order_data['customer_email'],
                customer_phone=order_data['customer_phone'],
                shipping_address=order_data['shipping_address'],
                subtotal = order_data['subtotal'],
                tax = order_data['tax'],
                discount_code=order_data.get('discount_code'),
                total_amount=order_data['total_amount']
            )
            
            for item in order_data['items']:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    subtotal=item['subtotal']
                )
            
            order_id = order.id
            
            if self.notifier:
                self.notifier.send_confirmation(
                    email=customer_data['email'],
                    order_id=order_id
                )
        
            return {
                'success': True,
                'order_id': order_id,
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
                
            