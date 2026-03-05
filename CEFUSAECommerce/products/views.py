from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.services import ProductService
from products.serializers import ProductSerializer, CreateProductSerializer

service = ProductService()

class ProductListCreateView(APIView):
    
    def get(self, request):
        filters = {'category': request.query_params.get('category')}
        products = service.list_products(filters)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product = service.create_product(serializer.validated_data)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
    
class ProductDetailView(APIView):
    
    def get(self, request, pk):
        try:
            product = service.get_product_details(pk)
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            product = service.get_product_details(pk)
            product.is_active = False
            product.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
class CheckStockView(APIView):
    
    def post(self, request):
        variant_id = request.data.get('variant_id')
        quantity = request.data.get('quantity')
        
        if not variant_id or not quantity:
            return Response({'error': 'variant_id y quantity son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = service.check_availability(variant_id, int(quantity))
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)