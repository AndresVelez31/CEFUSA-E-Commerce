# CEFUSAE-Commerce - Contexto Completo del Proyecto

## 📋 ÍNDICE

1. [Información General del Proyecto](#información-general-del-proyecto)
2. [Requisitos del Taller (Entregable 1)](#requisitos-del-taller-entregable-1)
3. [Modelo de Dominio](#modelo-de-dominio)
4. [Arquitectura y Principios SOLID](#arquitectura-y-principios-solid)
5. [Patrones de Diseño](#patrones-de-diseño)
6. [División del Trabajo (3 Personas)](#división-del-trabajo-3-personas)
7. [Plan de Implementación Paso a Paso](#plan-de-implementación-paso-a-paso)
8. [Interfaces y Contratos entre Módulos](#interfaces-y-contratos-entre-módulos)
9. [Estructura de Carpetas](#estructura-de-carpetas)
10. [Comandos y Setup](#comandos-y-setup)
11. [Checklist de Entregables](#checklist-de-entregables)
12. [Evaluación y Penalizaciones](#evaluación-y-penalizaciones)

---

## 🎯 INFORMACIÓN GENERAL DEL PROYECTO

### **¿Qué estamos construyendo?**
Un sistema de **e-commerce (CEFUSAE-Commerce)** usando Django y Django Rest Framework con arquitectura limpia, implementando el **60% de las clases de dominio** con patrones creacionales (Builder y Factory) y cumpliendo estrictamente los principios SOLID.

### **Contexto Académico**
- **Curso:** Arquitectura de Software 2026
- **Profesor:** Nicolás Ramírez Vélez
- **Entregable:** No. 1 - Núcleo de Negocio y Exposición de API Profesional
- **Equipo:** 3 personas
- **Nota máxima:** 5.0 puntos

### **Estado Actual del Proyecto**
- ✅ Django Rest Framework instalado
- ✅ App `orders` creada (básica)
- ✅ Modelos básicos: Order, OrderItem
- ✅ Builder y Factory implementados parcialmente
- 🔨 **FALTA:** Implementar el resto del modelo de dominio (60%)

---

## 📚 REQUISITOS DEL TALLER (ENTREGABLE 1)

### **1. Capa de Dominio (Avance del 50-60%)**

**Requisitos:**
- Implementar entre el **50% y 60%** de las clases del modelo de datos
- Usar **tipos de datos apropiados**
- Incluir **validaciones de negocio** en el nivel de modelo/entidad
- Los modelos deben ser coherentes con el diseño previo

**Peso en la nota:** 1.0 punto

---

### **2. Capa de Aplicación (Service Layer)**

**Requisitos ESTRICTOS:**
- ❌ **PROHIBIDO:** Lógica de negocio en Views o Serializers
- ✅ **OBLIGATORIO:** Cada flujo de negocio debe estar orquestado por una clase en `services.py`
- ✅ **OBLIGATORIO:** Cumplir con SOLID, especialmente SRP (Single Responsibility Principle)
- ✅ Desacoplamiento total mediante inyección de dependencias

**⚠️ ADVERTENCIA CRÍTICA:**
> Cualquier rastro de lógica de negocio (cálculos, validaciones de inventario, etc.) dentro de `views.py` o en métodos de un `Model` que no sean de persistencia **PENALIZARÁ la nota de SOLID en un 50%**

**Peso en la nota:** 1.5 puntos

---

### **3. Capa de Presentación (Django Rest Framework)**

**Requisitos:**
- Implementación de **Serializers** para entrada y salida de datos
- Uso de **APIView** para control total de la petición
- Manejo correcto de **códigos HTTP:**
  - `201` - Creado exitosamente
  - `400` - Bad Request (validación fallida)
  - `404` - No encontrado
  - `409` - Conflicto (ej: stock insuficiente)

**Peso en la nota:** 1.0 punto

---

### **4. Patrones Creacionales (OBLIGATORIOS)**

#### **Builder (Obligatorio)**
- Para la creación de la **entidad más compleja** del sistema
- En nuestro caso: **Order** (orden con items, descuentos, dirección)

#### **Factory (Obligatorio)**
- Para gestionar al menos **una dependencia externa** o variante de lógica
- En nuestro caso: 
  - **NotificationFactory** (MockNotifier vs EmailNotifier)
  - **PaymentProcessorFactory** (MockProcessor vs RealProcessor)

**Peso en la nota:** 1.0 punto

---

### **5. Documentación (Wiki de GitHub)**

**Requisitos:**
Documentación técnica que explique:

1. **Justificación de la estructura de carpetas elegida**
2. **Diagrama de secuencia** de la funcionalidad más compleja implementada
3. **Explicación de cómo el sistema está preparado para API Gateway** (Visión de escalabilidad)
4. **Explicación de patrones implementados** (Builder y Factory)
5. **Justificación de decisiones de diseño**

**Peso en la nota:** 0.5 puntos

---

### **6. Entregables**

La entrega se formaliza mediante **enlace al repositorio de GitHub** que contenga:
1. Código fuente en rama `main` o `develop`
2. Wiki técnica completa
3. README con instrucciones de instalación

---

## 🏗️ MODELO DE DOMINIO

### **Decisión Final: 60% = 6 Entidades Core**

Después de analizar el diagrama UML original y simplificarlo para ser funcional pero simple, decidimos implementar:

```
MODELO COMPLETO (100%): 9 entidades
IMPLEMENTAR AHORA (60%): 6 entidades
```

### **Entidades a Implementar (60%)**

#### **1. Product (Producto)**
```python
- name: CharField(max_length=150)
- description: TextField
- category: CharField(max_length=50)  # "Electrónica", "Ropa", etc.
- is_active: BooleanField(default=True)
- created_at: DateTimeField(auto_now_add=True)
```

**Responsabilidad:**
- Representa el producto base (ej: "Camiseta Nike")
- Puede tener múltiples variantes (tallas, colores)

---

#### **2. ProductVariant (VarianteProducto)**
```python
- product: ForeignKey(Product, related_name='variants')
- sku: CharField(max_length=50, unique=True)  # "CAM-NI-M-ROJA"
- size: CharField(max_length=20, null=True)   # "M", "L", "XL"
- color: CharField(max_length=30, null=True)  # "Rojo", "Azul"
- price: DecimalField(max_digits=10, decimal_places=2)
- is_available: BooleanField(default=True)
```

**Responsabilidad:**
- Representa una variante específica del producto
- Cada variante tiene su propio precio y disponibilidad
- Usado en e-commerce profesional (Amazon, MercadoLibre)

**Ejemplo:**
```
Producto: "Camiseta Nike"
  ├── Variante 1: SKU="CAM-NI-S-R", size="S", color="Rojo", price=29.99
  ├── Variante 2: SKU="CAM-NI-M-R", size="M", color="Rojo", price=29.99
  └── Variante 3: SKU="CAM-NI-L-A", size="L", color="Azul", price=34.99
```

---

#### **3. Inventory (Inventario)**
```python
- variant: OneToOneField(ProductVariant, related_name='inventory')
- cantidad_disponible: PositiveIntegerField(default=0)
- stock_minimo: PositiveIntegerField(default=5)
- updated_at: DateTimeField(auto_now=True)
```

**Responsabilidad:**
- Gestionar el stock de cada variante de producto
- Permitir validaciones de disponibilidad
- Separado del producto para facilitar auditorías

**Métodos de validación simples (permitidos en el modelo):**
```python
def tiene_stock(self, cantidad):
    return self.cantidad_disponible >= cantidad

def esta_bajo_minimo(self):
    return self.cantidad_disponible <= self.stock_minimo
```

---

#### **4. Customer (Cliente)**
```python
- nombre: CharField(max_length=100)
- apellido: CharField(max_length=100)
- email: EmailField(unique=True)
- telefono: CharField(max_length=20)
- direccion: TextField  # Dirección completa como texto
- created_at: DateTimeField(auto_now_add=True)
```

**Responsabilidad:**
- Información básica del cliente
- Por ahora SIN sistema de autenticación (compra como invitado)
- Se puede extender después con User de Django

---

#### **5. Order (Orden)**
```python
- customer: ForeignKey(Customer, related_name='orders')
- fecha_creacion: DateTimeField(auto_now_add=True)
- status: CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
  # Opciones: 'pending', 'confirmed', 'shipped', 'delivered', 'cancelled'
- direccion_envio: TextField
- discount_code: CharField(max_length=50, null=True, blank=True)
- subtotal: DecimalField(max_digits=10, decimal_places=2)
- discount_amount: DecimalField(max_digits=10, decimal_places=2, default=0)
- total: DecimalField(max_digits=10, decimal_places=2)

# Campos de envío integrados (sin entidad Shipping separada)
- shipping_status: CharField(max_length=20, default='pending')
  # Opciones: 'pending', 'preparing', 'shipped', 'delivered'
- tracking_number: CharField(max_length=100, null=True, blank=True)
```

**Responsabilidad:**
- Representa una compra/pedido
- Incluye información de envío integrada
- **Esta es la entidad más compleja** → Se usa Builder aquí

---

#### **6. OrderItem (DetalleOrden)**
```python
- order: ForeignKey(Order, related_name='items')
- variant: ForeignKey(ProductVariant, on_delete=models.PROTECT)
- product_name: CharField(max_length=150)  # Snapshot del nombre
- quantity: PositiveIntegerField()
- price: DecimalField(max_digits=10, decimal_places=2)  # Snapshot del precio
```

**Responsabilidad:**
- Detalle de cada producto en la orden
- Guarda snapshots (nombre y precio al momento de la compra)
- Protege contra cambios futuros en productos

---

### **Entidades para Después (40%)**

Estas se implementarán en iteraciones futuras:

7. **Cart** (Carrito) - Para agregar productos antes de comprar
8. **CartItem** - Items en el carrito
9. **Payment** (Pago) - Información de pagos y transacciones

---

### **Diagrama de Relaciones**

```
Product 1----* ProductVariant
ProductVariant 1----1 Inventory

Customer 1----* Order
Order 1----* OrderItem
OrderItem *----1 ProductVariant
```

**Flujo de negocio:**
1. Cliente navega productos y variantes
2. Cliente crea una orden con múltiples items
3. Sistema valida inventario
4. Se crea la orden y se actualizan los stocks

---

## 🏛️ ARQUITECTURA Y PRINCIPIOS SOLID

### **Arquitectura en Capas**

Nuestro sistema se divide en 3 capas bien diferenciadas:

```
┌─────────────────────────────────────────┐
│  CAPA DE PRESENTACIÓN                   │
│  (Django Rest Framework)                │
│                                         │
│  - APIViews / ViewSets                  │
│  - Serializers (validación I/O)         │
│  - Manejo de códigos HTTP               │
│  - NO lógica de negocio                 │
└─────────────────┬───────────────────────┘
                  │ delega
┌─────────────────▼───────────────────────┐
│  CAPA DE APLICACIÓN                     │
│  (Service Layer)                        │
│                                         │
│  - services.py                          │
│  - Lógica de negocio                    │
│  - Orquestación de operaciones          │
│  - Validaciones complejas               │
│  - Coordinación entre entidades         │
└─────────────────┬───────────────────────┘
                  │ usa
┌─────────────────▼───────────────────────┐
│  CAPA DE DOMINIO                        │
│  (Modelos y Builders)                   │
│                                         │
│  - models.py (solo persistencia)        │
│  - domain/builders.py (construcción)    │
│  - Validaciones simples de entidad      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  INFRAESTRUCTURA                        │
│  (Factories y externos)                 │
│                                         │
│  - infra/factories.py                   │
│  - Servicios externos                   │
│  - Implementaciones concretas           │
└─────────────────────────────────────────┘
```

---

### **Principios SOLID Aplicados**

#### **1. SRP - Single Responsibility Principle (Responsabilidad Única)**

**Principio:** Cada clase debe tener una sola razón para cambiar.

**Aplicación en el proyecto:**

❌ **INCORRECTO:**
```python
# views.py - Vista con TODO mezclado
class CreateOrderView(APIView):
    def post(self, request):
        # Validar datos
        # Calcular totales
        # Validar stock
        # Crear orden
        # Enviar email
        # Procesar pago
        # TODO EN UN SOLO LUGAR = VIOLA SRP
```

✅ **CORRECTO:**
```python
# views.py - Solo maneja HTTP
class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        # DELEGA al servicio
        service = OrderService()
        result = service.create_order(serializer.validated_data)
        
        if result['success']:
            return Response(result, status=201)
        return Response(result, status=400)

# services.py - Solo lógica de negocio
class OrderService:
    def __init__(self, notifier=None):
        self.notifier = notifier or NotificationFactory.create()
    
    def create_order(self, data):
        # Validar stock
        # Construir orden
        # Notificar
        # Retornar resultado
```

**Responsabilidades separadas:**
- **View:** Manejo de HTTP
- **Serializer:** Validación de datos
- **Service:** Lógica de negocio
- **Builder:** Construcción de objetos complejos
- **Factory:** Creación de dependencias

---

#### **2. OCP - Open/Closed Principle (Abierto/Cerrado)**

**Principio:** Abierto para extensión, cerrado para modificación.

**Aplicación con Factory:**

```python
# infra/factories.py
class NotificationFactory:
    @staticmethod
    def create():
        if settings.ENV_TYPE == 'development':
            return MockNotifier()
        elif settings.NOTIFY_METHOD == 'sms':
            return SMSNotifier()  # Nueva funcionalidad agregada
        return EmailNotifier()

# ✅ Puedes agregar SMSNotifier sin modificar código existente
```

---

#### **3. LSP - Liskov Substitution Principle**

**Principio:** Los objetos deben ser reemplazables por sus subtipos.

**Aplicación:**

```python
# Interfaz común (duck typing en Python)
class Notifier:
    def notify(self, user_email, message):
        raise NotImplementedError

class EmailNotifier:
    def notify(self, user_email, message):
        # Enviar email real
        pass

class MockNotifier:
    def notify(self, user_email, message):
        # Simular envío
        print(f"Mock: {message}")

# ✅ Ambos son intercambiables
```

---

#### **4. ISP - Interface Segregation Principle**

**Principio:** Los clientes no deben depender de interfaces que no usan.

**Aplicación:**
- Serializers específicos por operación (CreateOrderSerializer, ListOrderSerializer)
- Servicios especializados (ProductService, OrderService)

---

#### **5. DIP - Dependency Inversion Principle (Inversión de Dependencias)**

**Principio:** Depender de abstracciones, no de implementaciones concretas.

**Aplicación con Inyección de Dependencias:**

```python
class OrderService:
    def __init__(self, notifier=None, payment_processor=None):
        # Las dependencias se INYECTAN desde afuera
        self.notifier = notifier or NotificationFactory.create()
        self.payment_processor = payment_processor or PaymentProcessorFactory.create()
    
    def create_order(self, data):
        # Usa las dependencias inyectadas
        self.notifier.notify(...)
```

**Beneficios:**
- ✅ Fácil de testear (inyectas mocks)
- ✅ Fácil de cambiar implementaciones
- ✅ Bajo acoplamiento

---

## 🎨 PATRONES DE DISEÑO

### **1. Builder Pattern (Patrón Constructor)**

**¿Qué problema resuelve?**
Construir objetos complejos paso a paso con validaciones.

**¿Dónde lo usamos?**
Para construir **Order** (la entidad más compleja).

**¿Por qué Order es compleja?**
- Tiene múltiples items
- Necesita calcular totales
- Aplica descuentos
- Valida stock
- Crea snapshots de precios

**Implementación:**

```python
# orders/domain/builders.py
from decimal import Decimal
from orders.models import Order, OrderItem
from products.models import ProductVariant

class OrderBuilder:
    """
    Builder para construcción de órdenes complejas.
    Permite construir una orden paso a paso con validaciones.
    """
    
    def __init__(self):
        self._customer = None
        self._items = []  # Lista de {'variant': obj, 'quantity': int}
        self._shipping_address = None
        self._discount_code = None
    
    def for_customer(self, customer):
        """Establece el cliente de la orden"""
        self._customer = customer
        return self  # Fluent interface
    
    def add_item(self, variant, quantity):
        """
        Agrega un item a la orden.
        
        Args:
            variant: ProductVariant - Variante del producto
            quantity: int - Cantidad a ordenar
        
        Raises:
            ValueError: Si la cantidad es inválida o no hay stock
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        # Validar stock disponible
        if not variant.inventory.tiene_stock(quantity):
            raise ValueError(f"Stock insuficiente para {variant.product.name}")
        
        self._items.append({
            'variant': variant,
            'quantity': quantity
        })
        return self
    
    def with_shipping_address(self, address):
        """Establece la dirección de envío"""
        self._shipping_address = address
        return self
    
    def with_discount(self, discount_code):
        """Aplica un código de descuento"""
        self._discount_code = discount_code
        return self
    
    def build(self):
        """
        Construye y guarda la orden en la base de datos.
        
        Returns:
            Order: Orden creada y guardada
        
        Raises:
            ValueError: Si faltan datos obligatorios
        """
        # Validaciones finales
        if not self._customer:
            raise ValueError("Se requiere un cliente")
        
        if not self._items:
            raise ValueError("La orden debe tener al menos un item")
        
        if not self._shipping_address:
            raise ValueError("Se requiere dirección de envío")
        
        # Calcular subtotal
        subtotal = sum(
            item['variant'].price * item['quantity']
            for item in self._items
        )
        
        # Calcular descuento
        discount_amount = Decimal('0.00')
        if self._discount_code:
            # Esto se movería a un CouponService en producción
            if self._discount_code == 'SAVE10':
                discount_amount = subtotal * Decimal('0.10')
            elif self._discount_code == 'VIP20':
                discount_amount = subtotal * Decimal('0.20')
        
        # Calcular total
        total = subtotal - discount_amount
        
        # Crear la orden
        order = Order.objects.create(
            customer=self._customer,
            direccion_envio=self._shipping_address,
            discount_code=self._discount_code,
            subtotal=subtotal,
            discount_amount=discount_amount,
            total=total,
            status='pending'
        )
        
        # Crear los items de la orden
        for item in self._items:
            OrderItem.objects.create(
                order=order,
                variant=item['variant'],
                product_name=item['variant'].product.name,  # Snapshot
                quantity=item['quantity'],
                price=item['variant'].price  # Snapshot del precio
            )
            
            # Descontar del inventario
            inventory = item['variant'].inventory
            inventory.cantidad_disponible -= item['quantity']
            inventory.save()
        
        return order
```

**Uso del Builder:**

```python
# En el servicio
from orders.domain.builders import OrderBuilder

def create_order(customer, items_data, shipping_address, discount_code=None):
    builder = OrderBuilder()
    
    builder.for_customer(customer)
    
    for item_data in items_data:
        variant = ProductVariant.objects.get(id=item_data['variant_id'])
        builder.add_item(variant, item_data['quantity'])
    
    builder.with_shipping_address(shipping_address)
    
    if discount_code:
        builder.with_discount(discount_code)
    
    order = builder.build()  # ¡Orden completa y validada!
    return order
```

**Ventajas:**
- ✅ Fluent interface (encadenamiento de métodos)
- ✅ Validaciones paso a paso
- ✅ Código legible y expresivo
- ✅ Objeto garantizado válido después de `build()`

---

### **2. Factory Pattern (Patrón Fábrica)**

**¿Qué problema resuelve?**
Decidir qué implementación usar según el contexto.

**¿Dónde lo usamos?**
Para dependencias externas que cambian según el entorno.

**Implementación:**

#### **NotificationFactory**

```python
# orders/infra/notifiers.py

class MockNotifier:
    """Notificador para desarrollo - solo imprime en consola"""
    
    def notify(self, user_email: str, message: str) -> dict:
        print(f"[MOCK NOTIFICATION] To: {user_email}")
        print(f"[MOCK MESSAGE] {message}")
        return {
            'success': True,
            'method': 'mock',
            'recipient': user_email
        }


class EmailNotifier:
    """Notificador real - envía emails"""
    
    def notify(self, user_email: str, message: str) -> dict:
        # Aquí iría integración con SendGrid, AWS SES, etc.
        print(f"[REAL EMAIL] Sending to: {user_email}")
        # send_email(user_email, message)
        return {
            'success': True,
            'method': 'email',
            'recipient': user_email
        }


class SMSNotifier:
    """Notificador por SMS"""
    
    def notify(self, user_email: str, message: str) -> dict:
        # Aquí iría integración con Twilio, etc.
        print(f"[SMS] Sending to: {user_email}")
        return {
            'success': True,
            'method': 'sms',
            'recipient': user_email
        }
```

```python
# orders/infra/factories.py
from django.conf import settings
from .notifiers import MockNotifier, EmailNotifier, SMSNotifier

class NotificationFactory:
    """
    Factory que decide qué notificador usar según la configuración.
    
    - En desarrollo: MockNotifier (no envía emails reales)
    - En producción: EmailNotifier (envía emails reales)
    - Si se configura SMS: SMSNotifier
    """
    
    @staticmethod
    def create():
        env_type = getattr(settings, 'ENV_TYPE', 'development')
        notify_method = getattr(settings, 'NOTIFY_METHOD', 'email')
        
        if env_type == 'development':
            return MockNotifier()
        
        if notify_method == 'sms':
            return SMSNotifier()
        
        return EmailNotifier()
```

**Configuración en settings.py:**

```python
# Para desarrollo
ENV_TYPE = 'development'  # Usa MockNotifier

# Para producción
ENV_TYPE = 'production'
NOTIFY_METHOD = 'email'  # Usa EmailNotifier
```

**Uso en el Service:**

```python
from orders.infra.factories import NotificationFactory

class OrderService:
    def __init__(self, notifier=None):
        # Usa la factory si no se inyecta un notifier
        self.notifier = notifier or NotificationFactory.create()
    
    def create_order(self, data):
        # ... crear orden ...
        
        # Notificar al cliente
        self.notifier.notify(
            user_email=customer.email,
            message=f"¡Tu orden #{order.id} ha sido creada!"
        )
```

**Ventajas:**
- ✅ Cambias comportamiento con configuración
- ✅ No modificas código para cambiar implementación
- ✅ Fácil agregar nuevos notificadores (SMS, Push, etc.)
- ✅ Testing simple (inyectas mock)

---

## 👥 DIVISIÓN DEL TRABAJO (3 PERSONAS)

### **Estrategia de Trabajo Independiente**

Cada persona trabajará en **su propia rama Git** para evitar conflictos. Al final se integra todo.

```bash
# Persona 1
git checkout -b feature/products

# Persona 2
git checkout -b feature/customers-orders

# Persona 3
git checkout -b feature/integration-docs
```

---

### **👤 PERSONA 1: Módulo de Productos**

**Responsabilidad:** Sistema completo de productos, variantes e inventario.

#### **Apps asignadas:**
- `products/`

#### **Entidades:**
- ✅ Product
- ✅ ProductVariant
- ✅ Inventory

#### **Tareas específicas:**

1. **Crear modelos** (`products/models.py`)
   - Modelo `Product`
   - Modelo `ProductVariant`
   - Modelo `Inventory`
   - Relaciones entre modelos

2. **Crear Builder** (`products/domain/builders.py`)
   - `ProductBuilder` para crear productos con variantes
   - Validaciones de SKU único
   - Validaciones de stock inicial

3. **Crear Service** (`products/services.py`)
   - `ProductService` con métodos:
     - `create_product(data)` - Crea producto con variantes
     - `get_product_details(product_id)` - Detalle completo
     - `check_availability(variant_id, quantity)` - Verifica stock
     - `list_products(filters)` - Lista con filtros
     - `update_stock(variant_id, quantity)` - Actualiza inventario

4. **Crear Serializers** (`products/serializers.py`)
   - `ProductSerializer` - Para GET requests
   - `CreateProductSerializer` - Para POST requests
   - `ProductVariantSerializer`
   - `InventorySerializer`

5. **Crear Views** (`products/views.py`)
   - `ProductListCreateView(APIView)` - GET y POST
   - `ProductDetailView(APIView)` - GET, PUT, DELETE
   - `CheckStockView(APIView)` - POST para validar stock
   - **REGLA:** Vistas máximo 15 líneas, delegar todo al service

6. **Configurar URLs** (`products/urls.py`)
   ```python
   urlpatterns = [
       path('', ProductListCreateView.as_view()),
       path('<int:pk>/', ProductDetailView.as_view()),
       path('check-stock/', CheckStockView.as_view()),
   ]
   ```

7. **Crear estructura de carpetas**
   ```
   products/
   ├── models.py
   ├── services.py
   ├── serializers.py
   ├── views.py
   ├── urls.py
   ├── admin.py
   ├── tests.py
   ├── domain/
   │   ├── __init__.py
   │   └── builders.py
   └── infra/
       ├── __init__.py
       └── (vacío por ahora)
   ```

#### **Contrato de Interfaces (lo que otros necesitan de ti):**

```python
# products/services.py
class ProductService:
    def check_availability(self, variant_id, quantity):
        """
        Verifica si hay stock disponible.
        
        Returns:
            {
                'available': bool,
                'current_stock': int,
                'variant_name': str
            }
        """
        pass
    
    def reserve_stock(self, variant_id, quantity):
        """
        Reserva stock (descuenta del inventario).
        
        Returns:
            {
                'success': bool,
                'message': str
            }
        """
        pass
```

#### **Estimado de tiempo:** 4-5 horas

---

### **👤 PERSONA 2: Módulo de Clientes y Base de Órdenes**

**Responsabilidad:** Gestión de clientes y estructura base de órdenes.

#### **Apps asignadas:**
- `customers/`
- `orders/` (mejorar lo existente)

#### **Entidades:**
- ✅ Customer
- ✅ Order (modelo base)
- ✅ OrderItem (modelo base)

#### **Tareas específicas:**

1. **Crear app customers** y sus modelos
   - Modelo `Customer`
   - Validaciones de email único
   - Método de representación `__str__`

2. **Mejorar modelos de orders** (`orders/models.py`)
   - Actualizar modelo `Order`:
     - Agregar FK a `Customer`
     - Agregar FK a `ProductVariant` en OrderItem
     - Agregar campo `status`
     - Agregar campos de shipping integrados
   - Actualizar modelo `OrderItem`

3. **Crear Service de Customer** (`customers/services.py`)
   - `CustomerService` con métodos:
     - `create_customer(data)` - Registrar cliente
     - `get_customer_by_email(email)` - Buscar por email
     - `update_customer(customer_id, data)` - Actualizar
     - `get_customer_orders(customer_id)` - Historial

4. **Crear Serializers de Customer** (`customers/serializers.py`)
   - `CustomerSerializer`
   - `CreateCustomerSerializer`
   - Validación de email único

5. **Crear Views de Customer** (`customers/views.py`)
   - `CustomerListCreateView(APIView)`
   - `CustomerDetailView(APIView)`
   - `CustomerOrdersView(APIView)` - Ver órdenes del cliente

6. **Mejorar OrderService** (`orders/services.py`)
   - Actualizar `OrderService.create_order()` para usar el nuevo modelo
   - Integrar con `ProductService` para validar stock
   - Usar `OrderBuilder` existente (actualizado)

7. **Configurar URLs**
   - `customers/urls.py`
   - Actualizar `orders/urls.py` si es necesario

#### **Contrato de Interfaces:**

```python
# customers/services.py
class CustomerService:
    def get_or_create_customer(self, email, data):
        """
        Obtiene cliente existente o crea uno nuevo.
        
        Returns:
            Customer object
        """
        pass

# orders/services.py
class OrderService:
    def create_order(self, customer, items, shipping_address, discount_code=None):
        """
        Crea una orden completa.
        
        Args:
            customer: Customer object
            items: [{'variant_id': int, 'quantity': int}, ...]
            shipping_address: str
            discount_code: str (optional)
        
        Returns:
            {
                'success': bool,
                'order_id': int,
                'total': Decimal,
                'message': str
            }
        """
        pass
```

#### **Estimado de tiempo:** 4-5 horas

---

### **👤 PERSONA 3: Integración, Frontend React y Documentación**

**Responsabilidad:** Integrar todo, crear endpoint de checkout, desarrollar el frontend React, tests y documentación.

#### **Tareas específicas:**

1. **Actualizar OrderBuilder** (`orders/domain/builders.py`)
   - Integrar con los nuevos modelos
   - Validar con `ProductService.check_availability()`
   - Manejar descuentos
   - Crear snapshots correctos

2. **Crear endpoint de Checkout completo** (`orders/views.py`)
   - `CheckoutView(APIView)` - POST
   - Flujo:
     1. Recibir datos del cliente
     2. Validar productos y stock
     3. Crear/obtener cliente
     4. Crear orden usando OrderBuilder
     5. Enviar notificación
     6. Retornar respuesta

3. **Crear Serializers de Order** (`orders/serializers.py`)
   - `OrderSerializer` - Para GET
   - `CheckoutSerializer` - Para POST checkout
   - `OrderItemSerializer`

4. **Configurar URLs principal** (`CEFUSAECommerce/urls.py`)
   - Integrar todas las apps:
   ```python
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/products/', include('products.urls')),
       path('api/customers/', include('customers.urls')),
       path('api/orders/', include('orders.urls')),
   ]
   ```

5. **Configurar DRF en settings.py**
   ```python
   INSTALLED_APPS = [
       ...
       'rest_framework',
       'products',
       'customers',
       'orders',
   ]
   
   REST_FRAMEWORK = {
       'DEFAULT_RENDERER_CLASSES': [
           'rest_framework.renderers.JSONRenderer',
       ],
   }
   ```

6. **Crear tests básicos** (`orders/tests.py`, `products/tests.py`)
   - Test del flujo completo de checkout
   - Test de validación de stock
   - Test de Builder

7. **Documentación (Wiki de GitHub)**
   
   Crear páginas:
   
   **a) Home.md**
   - Descripción del proyecto
   - Tecnologías usadas
   - Instrucciones de instalación
   
   **b) Arquitectura.md**
   - Explicar las 3 capas
   - Diagrama de arquitectura
   - Justificación de estructura de carpetas
   
   **c) Patrones-de-Diseño.md**
   - Explicar Builder con código
   - Explicar Factory con código
   - Justificar por qué se eligieron
   
   **d) Diagrama-de-Secuencia.md**
   - Diagrama del flujo de Checkout
   - Explicación paso a paso
   
   **e) API-Gateway.md**
   - Explicar cómo está preparado para Gateway
   - Diagrama de escalabilidad futura
   
   **f) API-Endpoints.md**
   - Lista de todos los endpoints
   - Ejemplos de requests y responses

8. **Crear README.md** en la raíz
   ```markdown
   # CEFUSAE-Commerce
   
   ## Instalación
   ## Uso
   ## API Endpoints
   ## Equipo
   ```

9. **Frontend React con Vite + Tailwind CSS** (`frontend/`)

   El proyecto frontend ya está creado en `frontend/`. Tus responsabilidades son:

   **a) Ejecutar y verificar el frontend**
   ```bash
   cd frontend
   npm install        # instalar dependencias
   npm run dev        # servidor de desarrollo en http://localhost:3000
   ```

   **b) Estructura del proyecto frontend:**
   ```
   frontend/
   ├── src/
   │   ├── api/
   │   │   ├── axios.js          # Cliente HTTP con proxy a Django
   │   │   ├── products.js       # Llamadas a /api/products/
   │   │   ├── customers.js      # Llamadas a /api/customers/
   │   │   └── orders.js         # Llamadas a /api/orders/checkout/
   │   ├── context/
   │   │   └── CartContext.jsx   # Estado global del carrito (useReducer)
   │   ├── components/
   │   │   ├── layout/
   │   │   │   ├── Navbar.jsx    # Barra de navegación con contador del carrito
   │   │   │   └── Footer.jsx    # Pie de página
   │   │   ├── products/
   │   │   │   └── ProductCard.jsx  # Tarjeta de producto
   │   │   └── cart/
   │   │       └── CartItem.jsx  # Item editable en el carrito
   │   ├── pages/
   │   │   ├── HomePage.jsx            # Catálogo con búsqueda y filtros
   │   │   ├── ProductDetailPage.jsx   # Detalle + selección de variante
   │   │   ├── CartPage.jsx            # Carrito con resumen
   │   │   ├── CheckoutPage.jsx        # Formulario de compra
   │   │   └── OrderConfirmationPage.jsx  # Confirmación post-compra
   │   ├── App.jsx       # Rutas con react-router-dom
   │   ├── main.jsx      # Punto de entrada
   │   └── index.css     # Tailwind + clases personalizadas
   ├── vite.config.js    # Proxy /api → http://localhost:8000
   ├── tailwind.config.js
   └── package.json
   ```

   **c) Flujo de usuario implementado:**
   ```
   HomePage → ProductDetailPage → (Agregar al carrito)
                                        ↓
                               CartPage (revisar pedido)
                                        ↓
                              CheckoutPage (datos cliente)
                                        ↓
                          OrderConfirmationPage (orden creada)
   ```

   **d) Tecnologías del frontend:**
   - **React 18** + **Vite 5** (desarrollo rápido)
   - **Tailwind CSS 3** (estilo dark mode moderno)
   - **React Router v6** (navegación SPA)
   - **Axios** (peticiones HTTP al API Django)
   - **React Hot Toast** (notificaciones)
   - **Heroicons** (iconografía consistente)

   **e) Configuración del proxy (ya lista):**
   El archivo `vite.config.js` redirige automáticamente `/api/*` al backend Django en `localhost:8000`, por lo que no se necesita configurar CORS en desarrollo.

   **f) Tareas pendientes del frontend:**
   - [ ] Conectar `HomePage` con el endpoint real `/api/products/`
   - [ ] Verificar que `CheckoutPage` funcione con el endpoint `/api/orders/checkout/`
   - [ ] Ajustar los campos del formulario si el backend cambia la API
   - [ ] Agregar configuración CORS en Django para producción:
     ```bash
     pip install django-cors-headers
     ```
     ```python
     # settings.py
     INSTALLED_APPS = [..., 'corsheaders']
     MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
     CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
     ```
   - [ ] (Opcional) Agregar página de listado de órdenes del cliente

#### **Estimado de tiempo:** 7-9 horas (incluye frontend)

---

### **Reuniones de Sincronización Sugeridas:**

- **Día 1 (2 horas):** Setup inicial, definir interfaces, crear ramas
- **Día 2 (30 min):** Checkpoint - revisar avances
- **Día 3 (2 horas):** Integración y resolución de conflictos
- **Día 4 (2 horas):** Testing, documentación y entrega

---

## 📝 PLAN DE IMPLEMENTACIÓN PASO A PASO

### **FASE 0: Setup Inicial (Todos juntos)**

**Duración:** 30 minutos

#### **Paso 1: Crear las apps necesarias**

```bash
cd CEFUSAECommerce
python manage.py startapp products
python manage.py startapp customers
```

#### **Paso 2: Configurar settings.py**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # DRF
    'rest_framework',
    # Apps
    'products',
    'customers',
    'orders',
]

# Configuración DRF
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# Variable para Factory Pattern
ENV_TYPE = 'development'  # 'development' o 'production'
```

#### **Paso 3: Crear estructura de carpetas en cada app**

```bash
# Para products
mkdir products/domain
mkdir products/infra
touch products/domain/__init__.py
touch products/domain/builders.py
touch products/infra/__init__.py
touch products/serializers.py
touch products/urls.py

# Para customers
mkdir customers/domain
mkdir customers/infra
touch customers/domain/__init__.py
touch customers/infra/__init__.py
touch customers/serializers.py
touch customers/urls.py

# Para orders (ya existe, crear lo faltante)
mkdir orders/domain
mkdir orders/infra
touch orders/serializers.py
```

#### **Paso 4: Crear ramas Git**

```bash
git checkout -b develop  # Rama de desarrollo
git checkout -b feature/products
git checkout -b feature/customers-orders
git checkout -b feature/integration
```

#### **Paso 5: Definir interfaces base (contratos)**

Crear archivo `INTERFACES.md` con los contratos que cada módulo debe cumplir.

---

### **FASE 1: Desarrollo Paralelo (Cada uno en su rama)**

**Duración:** 4-5 horas

- Persona 1 trabaja en `feature/products`
- Persona 2 trabaja en `feature/customers-orders`
- Persona 3 espera y prepara documentación base

---

### **FASE 2: Primera Integración**

**Duración:** 1 hora

#### **Paso 1: Merge a develop**

```bash
git checkout develop
git merge feature/products
git merge feature/customers-orders
```

#### **Paso 2: Resolver conflictos si existen**

#### **Paso 3: Hacer migraciones**

```bash
python manage.py makemigrations
python manage.py migrate
```

#### **Paso 4: Probar modelos en shell**

```bash
python manage.py shell
```

```python
from products.models import Product, ProductVariant, Inventory
from customers.models import Customer

# Crear datos de prueba
product = Product.objects.create(
    name="Camiseta Nike",
    description="Camiseta deportiva",
    category="Ropa"
)

variant = ProductVariant.objects.create(
    product=product,
    sku="CAM-NI-M-R",
    size="M",
    color="Rojo",
    price=29.99
)

Inventory.objects.create(
    variant=variant,
    cantidad_disponible=100,
    stock_minimo=10
)
```

---

### **FASE 3: Integración Final y Testing**

**Duración:** 2-3 horas

- Persona 3 implementa Checkout
- Todos prueban el flujo completo
- Se crean tests

---

### **FASE 4: Documentación**

**Duración:** 2-3 horas

- Persona 3 crea la Wiki
- Persona 1 y 2 revisan y complementan
- Se crea el README

---

### **FASE 5: Entrega**

**Duración:** 30 minutos

- Push final a `main`
- Verificar que todo esté en GitHub
- Enviar enlace del repositorio

---

## 🔗 INTERFACES Y CONTRATOS ENTRE MÓDULOS

Para trabajar independientemente, necesitamos definir **qué espera cada módulo del otro**.

### **ProductService (Persona 1 implementa)**

```python
class ProductService:
    """Servicio para gestión de productos"""
    
    def check_availability(self, variant_id: int, quantity: int) -> dict:
        """
        Verifica disponibilidad de stock.
        
        Args:
            variant_id: ID de la variante
            quantity: Cantidad requerida
        
        Returns:
            {
                'available': bool,
                'current_stock': int,
                'variant_name': str,
                'price': Decimal
            }
        """
        pass
    
    def reserve_stock(self, variant_id: int, quantity: int) -> dict:
        """
        Reserva stock (descuenta del inventario).
        
        Args:
            variant_id: ID de la variante
            quantity: Cantidad a reservar
        
        Returns:
            {
                'success': bool,
                'message': str,
                'remaining_stock': int
            }
        """
        pass
    
    def get_variant_details(self, variant_id: int) -> dict:
        """
        Obtiene detalles de una variante.
        
        Returns:
            {
                'id': int,
                'sku': str,
                'product_name': str,
                'size': str,
                'color': str,
                'price': Decimal,
                'available': bool
            }
        """
        pass
```

### **CustomerService (Persona 2 implementa)**

```python
class CustomerService:
    """Servicio para gestión de clientes"""
    
    def get_or_create_customer(self, email: str, data: dict) -> Customer:
        """
        Obtiene cliente existente o crea uno nuevo.
        
        Args:
            email: Email del cliente
            data: {
                'nombre': str,
                'apellido': str,
                'telefono': str,
                'direccion': str
            }
        
        Returns:
            Customer object
        """
        pass
    
    def get_customer_by_email(self, email: str) -> Customer:
        """
        Busca cliente por email.
        
        Returns:
            Customer object or None
        """
        pass
```

### **OrderService (Persona 2 base, Persona 3 completa)**

```python
class OrderService:
    """Servicio para gestión de órdenes"""
    
    def __init__(self, notifier=None):
        self.notifier = notifier or NotificationFactory.create()
    
    def create_order(self, customer: Customer, items: list, 
                    shipping_address: str, discount_code: str = None) -> dict:
        """
        Crea una orden completa usando OrderBuilder.
        
        Args:
            customer: Customer object
            items: [
                {'variant_id': int, 'quantity': int},
                ...
            ]
            shipping_address: str
            discount_code: str (opcional)
        
        Returns:
            {
                'success': bool,
                'order_id': int,
                'total': Decimal,
                'message': str,
                'items_count': int
            }
        """
        pass
```

### **Ejemplo de uso integrado (Persona 3 implementa)**

```python
# orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.services import OrderService
from customers.services import CustomerService
from products.services import ProductService

class CheckoutView(APIView):
    def post(self, request):
        # 1. Extraer datos
        customer_data = request.data.get('customer')
        items_data = request.data.get('items')
        shipping_address = request.data.get('shipping_address')
        discount_code = request.data.get('discount_code')
        
        # 2. Validar stock (usa ProductService)
        product_service = ProductService()
        for item in items_data:
            availability = product_service.check_availability(
                item['variant_id'], 
                item['quantity']
            )
            if not availability['available']:
                return Response({
                    'success': False,
                    'message': f"Stock insuficiente para {availability['variant_name']}"
                }, status=409)
        
        # 3. Crear/obtener cliente (usa CustomerService)
        customer_service = CustomerService()
        customer = customer_service.get_or_create_customer(
            customer_data['email'],
            customer_data
        )
        
        # 4. Crear orden (usa OrderService)
        order_service = OrderService()
        result = order_service.create_order(
            customer=customer,
            items=items_data,
            shipping_address=shipping_address,
            discount_code=discount_code
        )
        
        # 5. Retornar respuesta
        if result['success']:
            return Response(result, status=201)
        return Response(result, status=400)
```

---

## 📁 ESTRUCTURA DE CARPETAS

```
CEFUSAE-Commerce/
├── venv/                           # Entorno virtual
├── CEFUSAECommerce/                # Proyecto Django
│   ├── CEFUSAECommerce/            # Configuración
│   │   ├── __init__.py
│   │   ├── settings.py            # Configuración principal
│   │   ├── urls.py                # URLs principales
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── products/                   # App de productos
│   │   ├── migrations/
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   └── builders.py        # ProductBuilder
│   │   ├── infra/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── models.py              # Product, ProductVariant, Inventory
│   │   ├── services.py            # ProductService
│   │   ├── serializers.py         # Serializers DRF
│   │   ├── views.py               # APIViews
│   │   ├── urls.py                # URLs de productos
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── customers/                  # App de clientes
│   │   ├── migrations/
│   │   ├── domain/
│   │   │   └── __init__.py
│   │   ├── infra/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── models.py              # Customer
│   │   ├── services.py            # CustomerService
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── orders/                     # App de órdenes
│   │   ├── migrations/
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   └── builders.py        # OrderBuilder ⭐
│   │   ├── infra/
│   │   │   ├── __init__.py
│   │   │   ├── factories.py       # NotificationFactory ⭐
│   │   │   ├── notifiers.py       # Mock/Email/SMS Notifiers
│   │   │   └── payment.py         # PaymentProcessor (si se usa)
│   │   ├── __init__.py
│   │   ├── models.py              # Order, OrderItem
│   │   ├── services.py            # OrderService
│   │   ├── serializers.py
│   │   ├── views.py               # CheckoutView
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests.py
│   │
│   ├── manage.py
│   └── db.sqlite3
│
├── frontend/                       # ⭐ FRONTEND REACT (Persona 3)
│   ├── src/
│   │   ├── api/
│   │   │   ├── axios.js            # Cliente Axios (proxy → Django)
│   │   │   ├── products.js
│   │   │   ├── customers.js
│   │   │   └── orders.js
│   │   ├── context/
│   │   │   └── CartContext.jsx     # Estado global del carrito
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   └── Footer.jsx
│   │   │   ├── products/
│   │   │   │   └── ProductCard.jsx
│   │   │   └── cart/
│   │   │       └── CartItem.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ProductDetailPage.jsx
│   │   │   ├── CartPage.jsx
│   │   │   ├── CheckoutPage.jsx
│   │   │   └── OrderConfirmationPage.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css               # Tailwind + componentes dark mode
│   ├── index.html
│   ├── vite.config.js              # Puerto 3000, proxy /api → :8000
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── package.json
│
├── .git/                          # Control de versiones
├── .gitignore
├── README.md                      # Instrucciones del proyecto
├── PROYECTO-CONTEXTO-COMPLETO.md  # Este documento
└── requirements.txt               # Dependencias Python
```

### **Justificación de la estructura:**

#### **Por App:**
- ✅ **Modularidad:** Cada app es independiente
- ✅ **Escalabilidad:** Fácil agregar nuevas apps
- ✅ **Separación de responsabilidades:** Cada app tiene su dominio claro

#### **Carpetas domain/ e infra/:**
- ✅ **domain/:** Patrones de dominio (Builders, entidades complejas)
- ✅ **infra/:** Patrones de infraestructura (Factories, servicios externos)
- ✅ **Arquitectura limpia:** Separación entre lógica de negocio y detalles técnicos

#### **services.py separado:**
- ✅ **Service Layer explícito:** No confundir con views o models
- ✅ **SOLID:** Principio de responsabilidad única
- ✅ **Testeable:** Fácil de testear sin HTTP

---

## 🚀 COMANDOS Y SETUP

### **Instalación inicial**

```bash
# 1. Clonar repositorio (si ya está en GitHub)
git clone <url-repo>
cd CEFUSAE-Commerce

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install django djangorestframework

# 5. Guardar dependencias
pip freeze > requirements.txt

# 6. Crear apps (si es necesario)
cd CEFUSAECommerce
python manage.py startapp products
python manage.py startapp customers

# 7. Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# 8. Crear superusuario para admin
python manage.py createsuperuser

# 9. Correr servidor Django
python manage.py runserver
```

### **Frontend React (Persona 3)**

```bash
# 1. Instalar dependencias del frontend
cd frontend
npm install

# 2. Correr servidor de desarrollo (http://localhost:3000)
npm run dev

# 3. Compilar para producción
npm run build

# Nota: el frontend hace proxy automático de /api/* hacia http://localhost:8000
# Asegúrate de que Django esté corriendo antes de usar el frontend
```

### **Correr backend + frontend juntos**

```bash
# Terminal 1 - Django
cd CEFUSAECommerce
python manage.py runserver

# Terminal 2 - React
cd frontend
npm run dev
```

### **Flujo de trabajo con Git**

```bash
# 1. Crear tu rama
git checkout -b feature/products  # o customers-orders o integration

# 2. Hacer cambios y commits frecuentes
git add .
git commit -m "feat: Implementar modelo Product"

# 3. Subir tu rama a GitHub
git push origin feature/products

# 4. Cuando termines, mergear a develop
git checkout develop
git merge feature/products

# 5. Al final, mergear develop a main
git checkout main
git merge develop
git push origin main
```

### **Comandos útiles de Django**

```bash
# Shell interactivo (probar modelos)
python manage.py shell

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver SQL de migraciones
python manage.py sqlmigrate products 0001

# Verificar problemas
python manage.py check

# Crear datos de prueba
python manage.py shell < scripts/populate_data.py
```

### **Testing**

```bash
# Correr todos los tests
python manage.py test

# Correr tests de una app
python manage.py test products

# Correr un test específico
python manage.py test products.tests.ProductModelTest
```

---

## ✅ CHECKLIST DE ENTREGABLES

### **Código (**60%**)**

#### **Modelos (1.0 punto)**
- [ ] Product implementado correctamente
- [ ] ProductVariant implementado correctamente
- [ ] Inventory implementado correctamente
- [ ] Customer implementado correctamente
- [ ] Order actualizado con nuevos campos
- [ ] OrderItem actualizado con FKs correctas
- [ ] Todas las relaciones (ForeignKey, OneToOne) correctas
- [ ] Validaciones de negocio en los modelos
- [ ] Migraciones aplicadas sin errores

#### **Service Layer (1.5 puntos)**
- [ ] ProductService implementado
- [ ] CustomerService implementado
- [ ] OrderService implementado
- [ ] **CRÍTICO:** NO hay lógica de negocio en views.py
- [ ] **CRÍTICO:** NO hay lógica de negocio compleja en models.py
- [ ] Inyección de dependencias en servicios
- [ ] Servicios son testeables
- [ ] Código cumple SRP (Single Responsibility)

#### **Django Rest Framework (1.0 punto)**
- [ ] Serializers para todos los modelos
- [ ] APIViews implementadas (no ViewSets)
- [ ] Códigos HTTP correctos:
  - [ ] 201 para creación exitosa
  - [ ] 400 para errores de validación
  - [ ] 404 para no encontrado
  - [ ] 409 para conflictos (ej: sin stock)
- [ ] Views delegan a services (máximo 15 líneas)
- [ ] Manejo de errores apropiado

#### **Patrones Creacionales (1.0 punto)**
- [ ] OrderBuilder implementado correctamente
- [ ] Builder usa fluent interface
- [ ] Builder valida antes de build()
- [ ] NotificationFactory implementado
- [ ] Factory cambia comportamiento según ENV_TYPE
- [ ] Código limpio y legible
- [ ] Patrones justificados en documentación

### **Documentación (0.5 puntos)**

#### **Wiki de GitHub**
- [ ] Página Home.md
  - [ ] Descripción del proyecto
  - [ ] Tecnologías
  - [ ] Instrucciones de instalación
- [ ] Página Arquitectura.md
  - [ ] Diagrama de capas
  - [ ] Justificación de estructura de carpetas
  - [ ] Explicación de separación de responsabilidades
- [ ] Página Patrones-de-Diseño.md
  - [ ] Builder explicado con código
  - [ ] Factory explicado con código
  - [ ] Justificación de por qué se eligieron
- [ ] Página Diagrama-de-Secuencia.md
  - [ ] Diagrama del flujo de Checkout
  - [ ] Explicación paso a paso
- [ ] Página API-Gateway.md
  - [ ] Visión de escalabilidad
  - [ ] Cómo está preparado el sistema
  - [ ] Diagrama futuro con Gateway

#### **README.md**
- [ ] Descripción del proyecto
- [ ] Requisitos (Python, Django)
- [ ] Instrucciones de instalación
- [ ] Instrucciones de uso
- [ ] Lista de endpoints
- [ ] Información del equipo

### **Git y Repositorio**

- [ ] Repositorio público en GitHub
- [ ] Commits semánticos (feat:, fix:, docs:)
- [ ] Historial de Git limpio
- [ ] Trabajo colaborativo evidente
- [ ] Código en rama main o develop
- [ ] .gitignore correcto (venv, db.sqlite3, __pycache__)

### **Testing (Opcional pero recomendado)**

- [ ] Tests del flujo de checkout
- [ ] Tests de Builder
- [ ] Tests de Factories
- [ ] Tests de validaciones

---

## ⚠️ EVALUACIÓN Y PENALIZACIONES

### **Rúbrica de Evaluación**

| Criterio | Peso | Indicadores de Logro |
|----------|------|----------------------|
| **Dominio y Avance** | 1.0 | Se implementó el 60% de las clases. Modelos coherentes con el diseño. |
| **SOLID y Service Layer** | 1.5 | Desacoplamiento total. Lógica en servicios. No Fat Views ni Fat Models. |
| **DRF y API Gateway** | 1.0 | Uso profesional de Serializers y APIViews. Wiki explica Gateway. |
| **Patrones Creacionales** | 1.0 | Builder y Factory correctos y justificados. Código limpio. |
| **Documentación (Wiki)** | 0.5 | Wiki completa con diagramas y justificaciones. |
| **TOTAL** | **5.0** | |

### **⛔ PENALIZACIONES CRÍTICAS**

#### **Penalización del 50% en SOLID (0.75 puntos perdidos)**

Se aplica si hay:

❌ **Lógica de negocio en views.py:**
```python
# ❌ PROHIBIDO
def create_order(request):
    total = sum(item.price * item.quantity for item in items)
    if total > 100:
        total *= 0.9  # Descuento - ¡ESTO ES LÓGICA DE NEGOCIO!
```

❌ **Métodos complejos en models.py:**
```python
# ❌ PROHIBIDO
class Order(models.Model):
    def calculate_total_with_discounts_and_taxes(self):
        # Lógica compleja - ¡ESTO NO VA AQUÍ!
        total = ...
        tax = ...
        discount = ...
        return total + tax - discount
```

#### **✅ LO QUE SÍ ESTÁ PERMITIDO:**

En **models.py**:
```python
class Order(models.Model):
    # ✅ Propiedades simples
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    # ✅ Métodos de representación
    def __str__(self):
        return f"Order #{self.id}"
    
    # ✅ Métodos de persistencia
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
```

En **views.py**:
```python
class OrderView(APIView):
    def post(self, request):
        # ✅ Solo validación y delegación
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        # ✅ DELEGA al servicio
        service = OrderService()
        result = service.create_order(serializer.validated_data)
        
        return Response(result, status=201)
```

### **Otras consideraciones**

- ❌ Código duplicado entre apps
- ❌ Hardcodear valores que deberían estar en configuración
- ❌ No manejar errores apropiadamente
- ❌ No usar tipos de datos correctos (ej: precio como Float en vez de Decimal)
- ❌ Commits con mensajes no descriptivos

---

## 🎓 CONCEPTOS CLAVE EXPLICADOS

### **¿Qué es un Service Layer y por qué es importante?**

El **Service Layer** es una capa que contiene toda la lógica de negocio de tu aplicación, separada de las vistas y los modelos.

**Analogía:**
Imagina un restaurante:
- **View (mesero):** Toma el pedido del cliente
- **Service (cocina):** Prepara la comida (lógica compleja)
- **Model (despensa):** Almacena los ingredientes

El mesero NO cocina, solo toma el pedido y lo lleva a la cocina.

**En código:**
```python
# View (mesero) - Solo recibe y retorna
class OrderView(APIView):
    def post(self, request):
        service = OrderService()  # Llama a la cocina
        result = service.create_order(request.data)
        return Response(result)

# Service (cocina) - Hace todo el trabajo
class OrderService:
    def create_order(self, data):
        # Validar
        # Calcular
        # Guardar
        # Notificar
        return {'success': True}

# Model (despensa) - Solo almacena
class Order(models.Model):
    total = models.DecimalField(...)
```

### **¿Qué es el Builder Pattern?**

Es un patrón para construir objetos complejos paso a paso.

**Sin Builder:**
```python
order = Order.objects.create(
    customer=customer,
    subtotal=calculate_subtotal(items),
    discount=calculate_discount(code),
    total=calculate_total(subtotal, discount),
    status='pending'
)
# Crear items
for item in items:
    OrderItem.objects.create(order=order, ...)
# ¡Mucho código repetido y propenso a errores!
```

**Con Builder:**
```python
builder = OrderBuilder()
order = builder.for_customer(customer)\
               .add_item(variant1, 2)\
               .add_item(variant2, 1)\
               .with_discount('SAVE10')\
               .build()
# ¡Legible, validado y completo!
```

### **¿Qué es el Factory Pattern?**

Es un patrón que decide qué implementación crear según el contexto.

**Sin Factory:**
```python
if ENV == 'dev':
    notifier = MockNotifier()
else:
    notifier = EmailNotifier()
# Este código se repetiría en muchos lugares
```

**Con Factory:**
```python
notifier = NotificationFactory.create()
# La factory decide internamente
```

**Beneficio:** Cambias el comportamiento desde `settings.py` sin tocar código.

---

## 📞 COMUNICACIÓN DEL EQUIPO

### **Canales recomendados:**

- **WhatsApp/Discord:** Comunicación rápida diaria
- **GitHub Issues:** Para reportar bugs o discutir features
- **GitHub Wiki:** Documentación técnica
- **Meetings:** Al menos 3 reuniones de sincronización

### **Comandos útiles para compartir:**

```bash
# Compartir tu branch
git push origin feature/tu-nombre

# Ver cambios de otros
git fetch origin
git checkout feature/otro-nombre

# Actualizar tu branch con cambios de develop
git checkout feature/tu-nombre
git merge develop
```

---

## 🎯 RESUMEN EJECUTIVO

### **Lo que tienes que lograr:**

1. ✅ **6 entidades** implementadas (60% del dominio)
2. ✅ **Service Layer** con toda la lógica de negocio
3. ✅ **Builder** para Order (entidad compleja)
4. ✅ **Factory** para Notifiers (dependencia externa)
5. ✅ **API REST** con DRF (Serializers + APIViews)
6. ✅ **Frontend React** dark mode moderno (Vite + Tailwind CSS)
7. ✅ **Wiki técnica** completa
8. ✅ **Código limpio** cumpliendo SOLID

### **División del trabajo:**

- **Persona 1:** Products (Product, ProductVariant, Inventory)
- **Persona 2:** Customers + Orders base (Customer, Order, OrderItem)
- **Persona 3:** Integración + Checkout + Frontend React + Documentación

### **Tiempo estimado:**

- **Setup:** 30 minutos
- **Desarrollo paralelo:** 4-5 horas
- **Integración:** 2-3 horas
- **Frontend React:** 3-4 horas *(Persona 3)*
- **Documentación:** 2-3 horas
- **Total:** ~12-15 horas

### **Nota final esperada:**

Si siguen este plan: **4.5 - 5.0 / 5.0** ✅

---

## 🚨 PREGUNTAS FRECUENTES

### **¿Qué hago si tengo conflictos en Git?**
```bash
git merge develop
# Si hay conflictos, Git te dirá qué archivos
# Abre los archivos, resuelve los conflictos manualmente
git add .
git commit -m "fix: Resolver conflictos con develop"
```

### **¿Puedo usar ViewSets en vez de APIView?**
Sí, pero el PDF menciona "APIView para control total". APIView es más explícito y cumple mejor el requisito.

### **¿Es obligatorio hacer tests?**
No está explícito en el PDF, pero es altamente recomendado. Ayuda en la calificación.

### **¿Cuánto debe medir una vista?**
El PDF dice "menos de 15 líneas" para SRP. Si tu vista tiene más, probablemente tiene lógica que debería estar en el Service.

### **¿Puedo usar async/await?**
Sí, pero no es necesario para este entregable. Mantén las cosas simples.

### **¿Debo deployar a producción?**
No, solo necesitas GitHub con el código. El deploy no es parte de este entregable.

---

## 📚 RECURSOS ADICIONALES

### **Documentación oficial:**
- Django: https://docs.djangoproject.com/
- Django Rest Framework: https://www.django-rest-framework.org/
- Python Decimal: https://docs.python.org/3/library/decimal.html

### **Patrones de diseño:**
- Refactoring Guru - Builder: https://refactoring.guru/design-patterns/builder
- Refactoring Guru - Factory: https://refactoring.guru/design-patterns/factory-method

### **SOLID:**
- Principios SOLID explicados: https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design

---

## ✍️ NOTAS FINALES

Este documento contiene **TODO** lo que necesitas saber para completar el proyecto exitosamente. 

**Si tienes dudas:**
1. Lee primero este documento completo
2. Consulta con el equipo
3. Pregunta al profesor si es necesario

**Recuerda:**
- ⭐ **SOLID es lo más importante** (1.5 puntos)
- ⭐ **NO pongas lógica en views** (penalización del 50%)
- ⭐ **Documenta todo en la Wiki**
- ⭐ **Commits frecuentes y descriptivos**

---

**¡Éxito en el proyecto!** 🚀

---

**Última actualización:** Marzo 4, 2026
**Versión:** 1.0
**Equipo:** CEFUSAE-Commerce Development Team
