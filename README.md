# BlitzBite — Backend

Django REST Framework backend powering [BlitzBite](../blitzbite), a food delivery application. It exposes a versioned JSON API under `/api/v1/` for restaurants, menus, cart, orders, promotions, reviews, favorites, notifications, and wallets, plus interactive API docs via **drf-spectacular**.

## Requirements

- Python 3.12+
- pip (use a virtual environment)

## Getting started

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Run the development server
python manage.py runserver
```

The API is now available at http://localhost:8000/api/v1/.

## API documentation

Interactive Swagger UI: http://localhost:8000/api/docs/
Raw OpenAPI schema: http://localhost:8000/api/schema/
Human-readable reference: [`API_DOCS.md`](API_DOCS.md)

## Authentication

Two authentication classes are enabled, tried in order:

1. **FirebaseAuthentication** — verifies a Firebase ID token from the `Authorization: Bearer <token>` header and upserts a local `User` keyed by `firebase_uid`.
2. **DevAuthentication** (testing only) — enabled by `USE_DEV_AUTH = True` in `config/settings.py`. Send `X-Dev-User-Id: <any-id>` and the user is created/looked up automatically:

```bash
curl -H "X-Dev-User-Id: test123" http://localhost:8000/api/v1/wallet/
```

> **Never enable `USE_DEV_AUTH` in any environment reachable by real users.**

## Project structure

```
config/           Django project settings, root URLs, auth classes,
                  shared StandardViewset (wraps responses in a
                  { status, data, meta } envelope), API routing
user/             Users, addresses, payment methods
restaurant/       Restaurants, categories, opening hours, addons
menu/             Menu categories, menu items, addon options
cart/             Cart and cart items
order/            Orders, order items, order timeline
promotion/        Promotions and coupons (+ coupon validation)
review/           Restaurant reviews and ratings
favorite/         User favorite restaurants
notification/     In-app notifications (+ mark-read)
wallet/           Wallet, transactions, top-up

<app>/api/        ViewSets for each app
<app>/models.py   Models
<app>/serializers.py
<app>/urls.py     DRF routers (incl. drf-nested-routers for
                  restaurant→menu-item→addon and user→address/payment routes)
```

All apps are mounted under `/api/v1/` via `config/api_urls.py`, with schema endpoints at `/api/schema/` and `/api/docs/`.

## Stack

- **Django 6** + **Django REST Framework**
- **djangorestframework-simplejwt**, **Firebase Admin** (token verification)
- **drf-spectacular** (OpenAPI 3 schema + Swagger UI)
- **django-filter**, **drf-nested-routers**, **django-cors-headers**
- **Pillow** (images), **python-dotenv**
- Database: SQLite (`db.sqlite3`) for development; see notes below

## Notes & roadmap

- The database is currently SQLite for local development; the API spec targets PostgreSQL in production.
- Currently implemented: cart/order flows, coupon validation, restaurant/menu CRUD (owner endpoints), reviews (tied to delivered orders), favorites, notifications, and wallet with top-up stubs.
- Planned: Celery + Redis background tasks (payment webhooks, promotion expiry, notifications), real payment gateway integration, PostgreSQL/Redis/S3 deployment, tests for checkout/coupon/wallet flows.
- Response envelope: `StandardViewset` in `config/viewsets.py` wraps successful responses as `{ status, data, meta }` (including pagination) — account for this when wiring the frontend.

## Testing

```bash
python manage.py test
```
