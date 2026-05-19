# Colmercia - Conecta con Colombia

Plataforma de comercio electrónico que conecta microempresarios colombianos con compradores interesados en productos culturales regionales.

## Stack Tecnológico

- **Backend**: Django 6.x + Django REST Framework (DRF)
- **Base de datos**: PostgreSQL (Neon)
- **Auth**: JWT con djangorestframework-simplejwt
- **Formato**: JSON REST API

## Estructura del Proyecto

```
colmercia/
├── accounts/           # Gestión de usuarios y autenticación
│   ├── models.py       # User (comprador, microempresario, admin)
│   ├── serializers.py # Registro, login, validación
│   ├── views.py        # API endpoints de auth
│   └── urls.py         # Rutas /api/accounts/
├── products/           # Catálogo de productos y regiones
│   ├── models.py       # Region, Product, Event
│   ├── serializers.py  # Serializers para API
│   ├── views.py        # ViewSets CRUD + filtros
│   └── urls.py         # Rutas /api/products/
├── orders/             # Carrito y pedidos
│   ├── models.py       # Cart, CartItem, Order, OrderItem
│   ├── serializers.py # Serializers
│   ├── views.py        # Cart + Order viewsets
│   └── urls.py         # Rutas /api/orders/
├── chatbot/            # Chatbot IA para recomendaciones
│   ├── services.py     # Lógica del chatbot
│   ├── views.py        # Endpoints de chat
│   └── urls.py         # Rutas /api/chatbot/
├── colmercia/          # Configuración del proyecto
│   ├── settings.py     # Settings Django + DRF + JWT
│   ├── urls.py         # URLs principales
│   └── wsgi.py         # WSGI config
└── manage.py
```

## Requisitos

```bash
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary
```

## Configuración

El proyecto está configurado para usar Neon (PostgreSQL cloud). Para desarrollo local, editar `colmercia/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_db',
        'USER': 'tu_user',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Migraciones

```bash
python manage.py migrate
```

## Ejecutar Servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

## Endpoints API

### Auth
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Registrar usuario |
| POST | `/api/accounts/login/` | Login (retorna JWT) |
| GET | `/api/accounts/me/` | Datos usuario actual |
| POST | `/api/auth/token/refresh/` | Refrescar token |

### Productos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET/POST | `/api/products/regions/` | Listar/Crear regiones |
| GET/POST | `/api/products/events/` | Eventos "Conecta con Colombia" |
| GET/POST | `/api/products/products/` | Catálogo de productos |
| GET | `/api/products/products/?region=uuid` | Filtrar por región |
| GET | `/api/products/products/?categoria=string` | Filtrar por categoría |

### Órdenes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/orders/cart/` | Crear/ver carrito |
| POST | `/api/orders/cart/add_item/` | Agregar producto al carrito |
| DELETE | `/api/orders/cart/remove_item/{id}/` | Eliminar item |
| POST | `/api/orders/` | Crear orden desde carrito |
| GET | `/api/orders/` | Ver mis órdenes |

### Chatbot IA
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/chatbot/chat/` | Enviar mensaje al chatbot |
| GET | `/api/chatbot/recommend/` | Recomendaciones por región |

**Ejemplo de uso del chatbot:**
```bash
# Chat general
curl -X POST http://localhost:8000/api/chatbot/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"hola"}'

# Recomendaciones por región
curl "http://localhost:8000/api/chatbot/recommend/?region=Cundinamarca"
```

## Datos de Prueba

```python
# Crear región
from products.models import Region
r = Region.objects.create(nombre='Cundinamarca', descripcion='...')

# Crear producto
from accounts.models import User
from products.models import Product
u = User.objects.first()
p = Product.objects.create(nombre='Sombrero Vueltiao', precio=45000, region=r, vendedor=u)
```

## Usuarios

- **Role**: MICROEMPRESARIO, COMPRADOR, ADMIN
- **Login**: Por email (no username)

## Pendiente (Fase 2)

- ✅ Chatbot IA para recomendaciones (implementado)
- Integración con pasarela de pagos
- Panel admin para microempresarios
- Historial cultural por producto