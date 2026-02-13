import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from orders.services import OrderService

#Vista para crear la orden -> la delega al OrderService
class CreateOrderView(View):
    def post(self, request):
        try:
            #Cargar la informacion
            data = json.loads(request.body)
            
            #Delegar al servicio
            service = OrderService()
            result = service.create_order(
                customer_data={
                    'name': data.get('customer_name'),
                    'email': data.get('customer_email'),
                    'phone': data.get('customer_phone')
                },
                items = data.get('items', []),
                shipping_address= data.get('shipping_address'),
                discount_code= data.get('discount_code')
            )
            
            #Retornar la respuesta
            status_code = 201 if result['success'] else 400
            return JsonResponse(result, status=status_code)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        
                                
        
    