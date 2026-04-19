# CEFUSA E-Commerce

> **Arquitectura de Software 2026-1** · Universidad  
> Backend Django + Microservicio Flask · Strangler Pattern

---

## Descripción

**CEFUSA E-Commerce** es una API backend que simula el proceso de compra de una tienda online. Está construida con **Django REST Framework** como monolito principal y evolucionada hacia una arquitectura híbrida mediante el **Strangler Pattern**, extrayendo el módulo de pagos a un microservicio **Flask** independiente orquestado con **Nginx** y **Docker**.

El proyecto abarca dos entregables:

| Entregable | Tema | Descripción |
|---|---|---|
| **E1** | Núcleo de negocio | Monolito Django con arquitectura por capas, Builder Pattern y Factory Pattern |
| **E2 (Taller 02)** | Strangler Pattern | Extracción del módulo de pagos a Flask, containerización Docker, ruteo con Nginx |

---

## Equipo

| Integrante | Responsabilidad principal |
|---|---|
| **Andres Velez** | Models, Builder Pattern, Microservicio Flask |
| **Sebastian Salazar** | Services, Factory Pattern, Docker + Nginx |
| **Nathalia Cardoza** | Integración, Tests y Documentación |

---

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Backend (monolito) | Python 3, Django, Django REST Framework |
| Microservicio de pagos | Python 3, Flask 3 |
| Base de datos | PostgreSQL 16 (Docker) / SQLite (local) |
| Reverse proxy | Nginx 1.27 |
| Containerización | Docker + Docker Compose |
| Frontend | React + Vite |
| Testing | pytest |

---

## Arquitectura del Sistema

### Entregable 1 — Monolito por Capas

```
┌─────────────────────────────────────────────────┐
│  Capa de Presentación (views.py + serializers.py) │  ← Solo HTTP
├─────────────────────────────────────────────────┤
│  Capa de Aplicación (services.py)                │  ← Lógica de negocio
├─────────────────────────────────────────────────┤
│  Capa de Dominio (models.py + domain/builders.py)│  ← Entidades + Builder
├─────────────────────────────────────────────────┤
│  Infraestructura (infra/factories.py + payment)  │  ← Dependencias externas
└─────────────────────────────────────────────────┘
```

> **Regla de oro:** Una vista nunca toca la BD directamente. Todo pasa por un Service.

### Entregable 2 — Arquitectura Híbrida (Strangler Pattern)

```
🌐 Cliente (Browser / React :3000)
        │
        ▼
⚙️  Nginx :80  (Reverse Proxy)
   ├── /api/v2/*  ──────────────▶  🔥 Flask :5000  (Payment Microservice)
   └── /          ──────────────▶  🐍 Django :8000  (Monolito Legacy)
                                           │
                                           ▼
                                   🗄️ PostgreSQL :5432
```

---

## Patrones de Diseño Implementados

### Builder Pattern

Construcción paso a paso de objetos complejos con validaciones intermedias.

**`OrderBuilder`** — construye una orden de compra con cliente, items, dirección y descuento:

```python
orden = (
    OrderBuilder()
    .for_customer(cliente)
    .with_shipping_address("Calle 123")
    .add_item(variant=variante, quantity=2)
    .with_discount("SAVE10")
    .build()  # valida, calcula totales y persiste
)
```

**`ProductBuilder`** — crea producto + variantes + inventario en un solo flujo:

```python
producto = (
    ProductBuilder()
    .with_name("Camiseta")
    .with_category("clothes")
    .add_variant(sku="CAM-S-BLA", price=45000, initial_stock=10, size="S", color="Blanco")
    .build()
)
```

### Factory Pattern

Selección de implementación según entorno (`ENV_TYPE: development | production`):

```
NotificationFactory.create()  →  MockNotifier (dev)  |  EmailNotifier (prod)
PaymentProcessorFactory.create()  →  MockPaymentProcessor (dev)  |  RealPaymentProcessor (prod)
```

`OrderService` no sabe si está usando un mock o uno real — principio **LSP + DIP**.

### Strangler Pattern (Taller 02)

Migración progresiva del módulo de pagos sin romper el monolito:

```
ANTES:  POST /api/orders/checkout/ → Django → OrderService (8 pasos)
DESPUÉS: POST /api/v2/checkout/   → Nginx  → Flask (microservicio aislado)
         POST /api/orders/checkout/ → Nginx  → Django (legacy intacto)
```

---

## Estructura del Proyecto

```
CEFUSAE-Commerce/
├── CEFUSAECommerce/                    # Backend Django
│   ├── CEFUSAECommerce/               # Config global (settings, urls)
│   ├── products/                      # Catálogo, variantes, inventario
│   │   ├── api/                       # Views + Serializers
│   │   ├── models.py                  # Product, ProductVariant, Inventory
│   │   ├── services.py                # ProductService
│   │   └── domain/builders.py         # ProductBuilder
│   ├── customers/                     # Clientes
│   │   ├── api/
│   │   ├── models.py                  # Customer
│   │   └── services.py               # CustomerService
│   └── orders/                        # Checkout + órdenes
│       ├── api/
│       ├── models.py                  # Order, OrderItem
│       ├── services.py               # OrderService (orquesta todo)
│       ├── domain/builders.py         # OrderBuilder
│       └── infra/
│           ├── factories.py           # NotificationFactory, PaymentProcessorFactory
│           ├── notifiers.py           # BaseNotifier, Mock, Email
│           └── payment.py             # BasePaymentProcessor, Mock, Real
│
├── flask_payment_service/             # Microservicio de pagos (Taller 02)
│   ├── app.py                         # Flask app con /api/v2/checkout/
│   ├── test_app.py                    # Tests de integración (pytest)
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                          # React + Vite
├── nginx/                             # Configuraciones Nginx
│   ├── nginx.conf                     # Config local
│   └── nginx.docker.conf              # Config Docker
│
├── Dockerfile                         # Imagen Django
├── docker-compose.yml                 # Orquestación 4 servicios
├── start.ps1                          # Script inicio local (Windows)
├── stop.ps1                           # Script detención
└── documentacion/
    ├── wiki_migracion_microservicios.md
    ├── plan_taller02.md
    └── explicacion_codigo.tex
```

---

## Modelos de Datos

| Entidad | Campos clave | Relación |
|---|---|---|
| `Product` | name, description, category, is_active | tiene → `ProductVariant` (1:N) |
| `ProductVariant` | sku, size, color, price | tiene → `Inventory` (1:1) |
| `Inventory` | available_quantity, minimum_stock | pertenece a → `ProductVariant` |
| `Customer` | nombre, apellido, email, telefono | tiene → `Order` (1:N) |
| `Order` | customer, status, subtotal, discount, total | tiene → `OrderItem` (1:N) |
| `OrderItem` | variant, product_name*, quantity, price* | pertenece a → `Order` |

> *Campos con `*` son **snapshots** del momento de la compra. Si el precio cambia, la orden histórica queda intacta.

---

## Flujo de Checkout (8 pasos)

```
1. Cliente envía POST /api/orders/checkout/
2. CheckoutSerializer valida el formato
3. OrderService.create_order() es invocado
4. CustomerService.get_or_create_customer() — obtiene o crea el cliente
5. OrderBuilder.for_customer().add_item().with_discount().build() — construye y persiste la orden
6. ProductService.reserve_stock() — descuenta stock de cada variante
7. PaymentProcessorFactory.create().process_payment() — procesa el pago
8. NotificationFactory.create().notify() — envía notificación al cliente
→ Retorna { success: true, order_id, total }
```

---

## API Endpoints

### Base URL: `http://localhost:8000/api/` (directo) o `http://localhost/api/` (Nginx)

#### Productos

| Método | Endpoint | Descripción | Respuesta |
|---|---|---|---|
| `GET` | `/api/products/` | Lista productos activos con variantes e inventario | 200 |
| `POST` | `/api/products/` | Crea producto (con variantes e inventario inicial) | 201 / 400 |
| `GET` | `/api/products/<id>/` | Detalle de producto | 200 / 404 |
| `PATCH` | `/api/products/<id>/` | Actualiza producto | 200 / 404 |
| `DELETE` | `/api/products/<id>/` | Desactiva producto (soft delete) | 204 / 404 |
| `POST` | `/api/products/check-stock/` | Verifica disponibilidad de una variante | 200 |

#### Clientes

| Método | Endpoint | Descripción | Respuesta |
|---|---|---|---|
| `GET` | `/api/customers/` | Lista clientes | 200 |
| `POST` | `/api/customers/` | Crea cliente | 201 / 409 |
| `GET` | `/api/customers/<id>/` | Detalle de cliente | 200 / 404 |
| `GET` | `/api/customers/<id>/orders/` | Órdenes de un cliente | 200 / 404 |

#### Órdenes

| Método | Endpoint | Descripción | Respuesta |
|---|---|---|---|
| `POST` | `/api/orders/checkout/` | Crea orden completa (checkout legacy) | 201 / 400 / 409 |
| `GET` | `/api/orders/<id>/` | Detalle de una orden | 200 / 404 |
| `PATCH` | `/api/orders/<id>/status/` | Cambia estado de la orden | 200 / 400 |

#### Admin

| Método | Endpoint | Descripción | Respuesta |
|---|---|---|---|
| `GET` | `/api/admin/dashboard/` | Estadísticas generales | 200 |
| `GET` | `/api/admin/orders/` | Listar todas las órdenes | 200 |
| `DELETE` | `/api/admin/orders/<id>/` | Eliminar una orden | 204 / 404 |

#### Microservicio Flask (nuevo — Taller 02)

| Método | Endpoint | Descripción | Respuesta |
|---|---|---|---|
| `POST` | `/api/v2/checkout/` | Checkout en microservicio Flask | 200 / 400 |
| `GET` | `/api/v2/health` | Health check del microservicio | 200 |
| `GET` | `/nginx-health` | Health check de Nginx | 200 |

**Ejemplo POST `/api/v2/checkout/`:**

```json
// Request
{ "amount": 150.0, "discount_code": "SAVE10", "order_reference": "ORD-42" }

// Response 200
{
  "success": true,
  "transaction_id": "MOCK-482031",
  "subtotal": 150.0,
  "discount_code": "SAVE10",
  "discount_amount": 15.0,
  "total": 135.0,
  "processor": "mock",
  "order_reference": "ORD-42"
}
```

---

## Principios SOLID Aplicados

| Principio | Dónde se aplica | Evidencia concreta |
|---|---|---|
| **S** — SRP | Todas las capas | Views ≠ Services ≠ Builders ≠ Factories |
| **O** — OCP | `NotificationFactory` | Agregar `SMSNotifier` sin tocar `OrderService` |
| **L** — LSP | `BaseNotifier`, `BasePaymentProcessor` | Mock y Real son intercambiables |
| **I** — ISP | Serializers | `Create` / `Update` / `Read` separados |
| **D** — DIP | `OrderService.__init__` | `notifier=None` acepta inyección desde fuera |

---

## Guía de Instalación y Ejecución

### Opción 1 — Docker Compose (recomendada)

```bash
# Clonar el repositorio
git clone https://github.com/AndresVelez31/CEFUSA-E-Commerce.git
cd CEFUSA-E-Commerce

# Levantar todos los servicios (Django + Flask + PostgreSQL + Nginx)
docker compose up --build

# Cargar datos de prueba (en otra terminal)
docker compose exec django_app sh -lc "cd /app/CEFUSAECommerce ; python seed_products.py"
docker compose exec django_app sh -lc "cd /app/CEFUSAECommerce ; python seed_customers_orders.py"

# Detener
docker compose down
```

Accesos:
- **Frontend / API:** `http://localhost` (via Nginx)
- **Django directo:** `http://localhost:8000`
- **Flask directo:** `http://localhost:5000`

### Opción 2 — Scripts PowerShell (Windows local)

```powershell
# Iniciar Django + Flask + Nginx
.\start.ps1

# Detener
.\stop.ps1
```

### Opción 3 — Manual (desarrollo)

```bash
# Backend Django
cd CEFUSAECommerce
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Microservicio Flask (otra terminal)
cd flask_payment_service
pip install flask pytest
python app.py

# Frontend (otra terminal)
cd frontend
npm install
npm run dev
```

---

## Tests

### Tests del microservicio Flask

```bash
cd flask_payment_service
python -m pytest test_app.py -v
```

**Casos cubiertos:**
- Health check (HTTP 200, body correcto)
- Checkout sin descuento → total = amount
- Checkout con descuento → 10% aplicado
- Presence de `transaction_id` en la respuesta
- `order_reference` se refleja en la respuesta
- Sin body → HTTP 400
- Sin `amount` → HTTP 400
- `amount` no numérico → HTTP 400
- `amount` negativo → HTTP 400
- `amount` cero → HTTP 400

---

## Wiki del Proyecto

La documentación técnica completa del Taller 02 (Strangler Pattern) se encuentra en:

📄 [`documentacion/wiki_migracion_microservicios.md`](documentacion/wiki_migracion_microservicios.md)

Incluye: matriz de decisión, diagrama de arquitectura, snippets de Nginx, evidencia de pruebas y tabla de cumplimiento de la rúbrica.

---

## Notas Técnicas

> **¿Flask necesita acceso a la BD de Django?**  
> No. El microservicio Flask solo procesa montos y retorna `transaction_id`. La `Order` sigue creándose en Django; Flask maneja únicamente el cálculo financiero.

> **¿Por qué no se modificó `/api/v1/checkout/`?**  
> El Strangler Pattern exige que el servicio legacy no se rompa. Django sigue funcionando sin cambios. La nueva funcionalidad se expone en `/api/v2/`.

> **¿Cómo agregar un nuevo procesador de pago?**  
> 1. Crear `StripePaymentProcessor(BasePaymentProcessor)` con su `process_payment()`.  
> 2. Ajustar `PaymentProcessorFactory.create()`.  
> 3. Nada más. `OrderService`, las vistas y los serializers no cambian — **OCP en acción**.
