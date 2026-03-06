from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.services import ProductService
from products.serializers import (
    ProductSerializer,
    ProductVariantSerializer,
    CreateProductSerializer,
    CreateVariantSerializer,
    UpdateProductSerializer,
    UpdateVariantSerializer,
    UpdateStockSerializer,
)


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTOS
# ══════════════════════════════════════════════════════════════════════════════

class ProductListCreateView(APIView):
    """
    GET  /api/products/           → lista productos activos (filtro: ?category=)
    POST /api/products/           → crea un producto con sus variantes
    """

    def get(self, request):
        service = ProductService()
        filters = {'category': request.query_params.get('category')}
        products = service.list_products(filters)
        return Response(ProductSerializer(products, many=True).data)

    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = ProductService().create_product(serializer.validated_data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    """
    GET    /api/products/<pk>/    → detalle completo
    PATCH  /api/products/<pk>/    → actualiza campos del producto
    DELETE /api/products/<pk>/    → baja lógica (is_active=False)
    """

    def get(self, request, pk):
        try:
            product = ProductService().get_product_details(pk)
            return Response(ProductSerializer(product).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        serializer = UpdateProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = ProductService().update_product(pk, serializer.validated_data)
        if not result['success']:
            return Response({'error': result['message']}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(result['product']).data)

    def delete(self, request, pk):
        result = ProductService().deactivate_product(pk)
        if not result['success']:
            return Response({'error': result['message']}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ══════════════════════════════════════════════════════════════════════════════
# VARIANTES
# ══════════════════════════════════════════════════════════════════════════════

class ProductVariantListCreateView(APIView):
    """
    GET  /api/products/<pk>/variants/  → lista variantes del producto
    POST /api/products/<pk>/variants/  → añade una nueva variante
    """

    def get(self, request, pk):
        try:
            product = ProductService().get_product_details(pk)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        variants = product.variants.select_related('inventory').all()
        return Response(ProductVariantSerializer(variants, many=True).data)

    def post(self, request, pk):
        serializer = CreateVariantSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = ProductService().add_variant_to_product(pk, serializer.validated_data)
        if not result['success']:
            # 409 si el SKU ya existe, 404 si el producto no existe
            err_status = (
                status.HTTP_409_CONFLICT
                if 'SKU' in result['message']
                else status.HTTP_404_NOT_FOUND
            )
            return Response({'error': result['message']}, status=err_status)
        return Response(
            ProductVariantSerializer(result['variant']).data,
            status=status.HTTP_201_CREATED
        )


class ProductVariantDetailView(APIView):
    """
    GET    /api/products/variants/<vpk>/  → detalle de la variante
    PATCH  /api/products/variants/<vpk>/  → actualiza campos de la variante
    DELETE /api/products/variants/<vpk>/  → elimina la variante
    """

    def get(self, request, vpk):
        try:
            variant = ProductService().get_variant(vpk)
            return Response(ProductVariantSerializer(variant).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, vpk):
        serializer = UpdateVariantSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = ProductService().update_variant(vpk, serializer.validated_data)
        if not result['success']:
            err_status = (
                status.HTTP_409_CONFLICT
                if 'SKU' in result['message']
                else status.HTTP_404_NOT_FOUND
            )
            return Response({'error': result['message']}, status=err_status)
        return Response(ProductVariantSerializer(result['variant']).data)

    def delete(self, request, vpk):
        result = ProductService().delete_variant(vpk)
        if not result['success']:
            err_status = (
                status.HTTP_409_CONFLICT
                if 'ordenes' in result['message']
                else status.HTTP_404_NOT_FOUND
            )
            return Response({'error': result['message']}, status=err_status)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ══════════════════════════════════════════════════════════════════════════════
# INVENTARIO
# ══════════════════════════════════════════════════════════════════════════════

class VariantStockView(APIView):
    """
    PATCH /api/products/variants/<vpk>/stock/
    Body: { "quantity": 50 }  → establece el stock absoluto de la variante
    """

    def patch(self, request, vpk):
        serializer = UpdateStockSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = ProductService().update_stock(
                variant_id=vpk,
                quantity=serializer.validated_data['quantity']
            )
            return Response(result)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


class CheckStockView(APIView):
    """
    POST /api/products/check-stock/
    Body: { "variant_id": 3, "quantity": 2 }
    """

    def post(self, request):
        variant_id = request.data.get('variant_id')
        quantity   = request.data.get('quantity')
        if not variant_id or not quantity:
            return Response(
                {'error': 'variant_id y quantity son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            result = ProductService().check_availability(variant_id, int(quantity))
            return Response(result)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
