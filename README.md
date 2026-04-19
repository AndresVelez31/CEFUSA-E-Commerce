<div align="center">

# 🛍️ CEFUSA E-Commerce
</div >

---

## Descripción

**CEFUSA E-Commerce** es una API backend que simula el proceso de compra de una tienda online. Está construida con **Django REST Framework** como monolito principal y evolucionada hacia una arquitectura híbrida mediante el **Strangler Pattern**, extrayendo el módulo de pagos a un microservicio **Flask** independiente orquestado con **Nginx** y **Docker**.


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

### Entregable 2 — Strangler Pattern

```
🌐 Cliente
    │
    ▼
⚙️  Nginx :80
   ├── /api/v2/*  ──▶  🔥 Flask :5000  (Payment Microservice)
   └── /*         ──▶  🐍 Django :8000  (Monolito Legacy)
                               │
                               ▼
                        🗄️ PostgreSQL
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

### 🔥 Microservicio Flask (nuevo)
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/v2/checkout/` | Checkout en Flask (sin BD) |
| `GET` | `/api/v2/health` | Health check |

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
# Seed de datos de prueba
docker compose exec django_app sh -lc "cd /app/CEFUSAECommerce ; python seed_products.py"
docker compose exec django_app sh -lc "cd /app/CEFUSAECommerce ; python seed_customers_orders.py"
```

| Servicio | URL |
|---|---|
| API via Nginx | `http://localhost` |
| Django directo | `http://localhost:8000` |
| Flask directo | `http://localhost:5000` |
| Frontend | `http://localhost:3000` |

### 💻 Local (Windows)

```powershell
.\start.ps1   # inicia Django + Flask + Nginx
.\stop.ps1    # detiene todo
```

---

## 🧪 Tests

```bash
cd flask_payment_service
python -m pytest test_app.py -v
```

✅ Cubre: health check · checkout con/sin descuento · errores 400 estructurados

---

## 📚 Documentación

📖 [Wiki — Migración a Microservicios (Strangler Pattern)](https://github.com/AndresVelez31/CEFUSA-E-Commerce/wiki/Taller-02-%E2%80%90-Migraci%C3%B3n-a-Microservicios-(Strangler-Pattern).)

---
