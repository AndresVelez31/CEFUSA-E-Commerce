<div align="center">

# 🛍️ CEFUSA E-Commerce
</div >

---

## Descripción

**CEFUSA E-Commerce** es una API backend que simula el proceso de compra de una tienda online. Está construida con **Django REST Framework** como monolito principal y evolucionada hacia una arquitectura híbrida mediante el **Strangler Pattern**, extrayendo múltiples capacidades a microservicios **Flask** (payments, inventory, cart, customers, shipping) orquestados con **Nginx** y **Docker**, con **Redis + Celery** para tareas asíncronas.


---

## 👥 Equipo

| Integrante |
|---|
| 🧑‍💻 Andres Velez | 
| 🧑‍💻 Sebastian Salazar | 
| 🧑‍💻 Nathalia Cardoza | 

---

## 🧱 Stack Tecnológico

| Capa | Tecnología |
|---|---|
| 🐍 Backend monolito | Python 3 · Django · Django REST Framework |
| 🔥 Microservicio | Python 3 · Flask 3 |
| 🗄️ Base de datos | PostgreSQL 16 |
| ⚙️ Proxy / Ruteo | Nginx 1.27 |
| 📮 Broker / Async | Redis · Celery |
| 🐳 Contenedores | Docker · Docker Compose |
| 🌐 Frontend | React · Vite |
| 🧪 Testing | pytest |

---

## 🏛️ Arquitectura

### Entregable 1 — Monolito por Capas

```
┌─────────────────────────────────────────────┐
│  🖥️  Presentación   views.py · serializers  │
├─────────────────────────────────────────────┤
│  ⚙️  Aplicación     services.py             │
├─────────────────────────────────────────────┤
│  📐  Dominio        models.py · builders    │
├─────────────────────────────────────────────┤
│  🔌  Infraestructura factories · notifiers  │
└─────────────────────────────────────────────┘
```

### Entregable 2 — Strangler Pattern (Microservicios)

```
🌐 Cliente
    │
    ▼
⚙️  Nginx :80
   ├── /api/v2/checkout/   ──▶  🔥 ms-payment   :5000
   ├── /api/v2/products/   ──▶  🔥 ms-inventory :5001
   ├── /api/v2/inventory/  ──▶  🔥 ms-inventory :5001
   ├── /api/v2/cart/       ──▶  🔥 ms-cart      :5002
   ├── /api/v2/customers/  ──▶  🔥 ms-customers :5003
   ├── /api/v2/shipping/   ──▶  🔥 ms-shipping  :5004
   └── /api/* y /          ──▶  🐍 Django :8000 (Monolito Legacy)
                               │
                               ▼
                        🗄️ PostgreSQL
                        📮 Redis + ⚡ Celery
```

El monolito **no se rompe ni se modifica**. Nginx bifurca el tráfico según la versión de la ruta.

---

## 🎨 Patrones de Diseño

### 🔨 Builder Pattern
Construcción validada paso a paso de órdenes y productos.

```python
orden = (
    OrderBuilder()
    .for_customer(cliente)
    .add_item(variant, quantity=2)
    .with_discount("SAVE10")
    .build()  # valida, calcula totales y persiste
)
```

### 🏭 Factory Pattern
Selección de implementación según entorno (`development` / `production`).

```
PaymentProcessorFactory.create()  →  MockPaymentProcessor  (dev)
                                  →  RealPaymentProcessor   (prod)

NotificationFactory.create()      →  MockNotifier           (dev)
                                  →  EmailNotifier          (prod)
```

### 🐍 Strangler Pattern
Migración progresiva sin detener el sistema:

```
ANTES:  POST /api/orders/checkout/  →  Django  (8 pasos)
AHORA:  POST /api/v2/checkout/      →  Flask   (cálculo aislado, sin BD)
```

---

## 📡 Endpoints Principales

### 🛒 Órdenes (Django legacy)
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/orders/checkout/` | Crear orden completa |
| `GET` | `/api/orders/<id>/` | Detalle de orden |
| `PATCH` | `/api/orders/<id>/status/` | Cambiar estado |

### 🏷️ Productos
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/products/` | Listar productos activos |
| `POST` | `/api/products/` | Crear producto |
| `POST` | `/api/products/check-stock/` | Verificar stock |

### 👤 Clientes
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/customers/` | Listar clientes |
| `POST` | `/api/customers/` | Crear cliente |
| `GET` | `/api/customers/<id>/orders/` | Órdenes del cliente |

### 🔥 Microservicios v2 (Flask)
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/v2/checkout/` | Checkout en Flask (sin BD) |
| `GET` | `/api/v2/products/` | Listar productos (ms-inventory) |
| `POST` | `/api/v2/cart/<cart_id>/items/` | Agregar item al carrito (ms-cart) |
| `GET` | `/api/v2/customers/` | Listar clientes (ms-customers) |
| `POST` | `/api/v2/shipping/` | Crear envío (ms-shipping) |

### 🔗 Integraciones (API pública)
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/public/stats/` | Estadísticas públicas del sistema |
| `GET` | `/api/integrations/exchange-rate/` | Tasa de cambio (Adapter) |
| `GET` | `/api/integrations/ally/` | Servicio del aliado (Adapter) |
| `GET` | `/api/integrations/quickbite/info/` | Proxy a API externa QuickBite |

**Ejemplo `/api/v2/checkout/`:**
```json
// Request
{ "amount": 150.0, "discount_code": "SAVE10", "order_reference": "ORD-1" }

// Response 200
{ "success": true, "transaction_id": "MOCK-482031", "total": 135.0 }
```

---

## 🚀 Cómo correr el proyecto

### 🐳 Docker (recomendado)

```bash
docker compose up --build
```

```bash
# Catálogo (tienda + admin productos → ms-inventory)
docker compose exec ms_inventory python seed_products.py

# Órdenes de demo en Django (opcional, admin órdenes)
docker compose exec django_app sh -lc "cd /app/CEFUSAECommerce ; python seed_customers_orders.py"
```

| Servicio | URL | Rol |
|---|---|---|
| API via Nginx | `http://localhost` | **Usar siempre desde el frontend** |
| ms-inventory | `http://localhost:5001` | Productos / stock |
| ms-cart | `http://localhost:5002` | Carrito |
| ms-customers | `http://localhost:5003` | Clientes |
| ms-shipping | `http://localhost:5004` | Envíos |
| flask-payment | `http://localhost:5000` | Pagos (vía Django checkout) |
| Django | `http://localhost:8000` | Órdenes y admin |
| Redis | `http://localhost:6379` | Broker Celery |
| Frontend | `http://localhost:3000` | React (proxy → Nginx) |

### 💻 Local (Windows)

```powershell
.\start.ps1   # inicia Django + Flask + Nginx
.\stop.ps1    # detiene todo
```

---

## 🧪 Tests

```bash
cd services/flask_payment_service && python -m pytest test_app.py -v
cd ../flask_inventory_service && python -m pytest test_app.py -v
cd ../flask_cart_service && python -m pytest test_app.py -v
cd ../flask_customers_service && python -m pytest test_app.py -v
cd ../flask_shipping_service && python -m pytest test_app.py -v
```

✅ Cubre: health check · checkout con/sin descuento · errores 400 estructurados

---

## 📚 Documentación

📖 [Wiki — Migración a Microservicios (Strangler Pattern)](https://github.com/AndresVelez31/CEFUSA-E-Commerce/wiki/Taller-02-%E2%80%90-Migraci%C3%B3n-a-Microservicios-(Strangler-Pattern).)

---
