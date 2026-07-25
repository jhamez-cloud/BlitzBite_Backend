# BlitzBite Backend API Specification

This document specifies the Django + Django REST Framework backend needed to power the BlitzBite frontend and replace all mock data.

## Overview
- Project: Django REST API (PostgreSQL) with Celery+Redis for background tasks, optional Channels for realtime.
- API version: `/api/v1/`
- Auth: JWT (djangorestframework-simplejwt)

## Apps
- `users` — authentication, profiles, addresses, payment methods, preferences
- `restaurants` — restaurants, categories, opening hours
- `menu` — menu items, addons, menu categories
- `cart` — persistent shopping cart and items
- `orders` — orders, order items, timeline, couriers
- `promotions` — promotions, coupons
- `reviews` — reviews, rating summaries
- `favorites` — user favorites (restaurants)
- `notifications` — in-app notifications
- `wallet` — user wallet and transactions
- `search` — search helpers/indexing (optional)

## Models (summary with fields)

### users.User (extends AbstractUser)
- `id`: Auto
- `email`: EmailField (unique)
- `name`: CharField
- `phone`: CharField
- `avatar`: URLField / ImageField (nullable)
- `joined_date`: DateTime
- `total_orders`: Integer
- `total_spent`: Decimal
- `preferences`: JSONField (notifications/theme)

### users.Address
- `id`, `user` FK, `label`, `address` (text), `lat`/`lng` optional, `is_default` boolean

### users.PaymentMethod
- `id`, `user` FK, `type` (mobile_money|card|wallet), `label`, `details` JSON, `is_default`, `icon`

### restaurants.Restaurant
- `id`, `name`, `slug`, `logo`, `banner`, `rating` Decimal, `review_count` int
- `delivery_time` (string or int minutes), `delivery_fee` Decimal, `minimum_order` Decimal
- `categories` M2M to RestaurantCategory, `is_open`, `is_featured`, `is_trending`
- `address`, `description`, `phone`

### restaurants.OpeningHours
- `id`, `restaurant` FK, `day` (int/str), `open_time`, `close_time`

### restaurants.RestaurantCategory
- `id`, `name`, `slug`, `icon`, `image`, `count` (cached)

### menu.MenuCategory
- `id`, `name`, `slug`

### menu.MenuItem
- `id`, `restaurant` FK, `name`, `description`, `price` Decimal, `image`, `category` FK
- `available` boolean, `calories` int nullable, `is_popular` boolean
- `addons`: M2M to Addon (through table to store required/optional)

### menu.Addon
- `id`, `name`, `price` Decimal

### cart.Cart
- `id` UUID, `user` FK nullable, `session_key` nullable, `subtotal`, `delivery_fee`, `discount`, `tip`, `total` Decimals

### cart.CartItem
- `id` UUID, `cart` FK, `menu_item` FK, `restaurant` FK, `name`, `price`, `image`, `quantity`, `selected_addons` JSON or M2M, `special_instructions`

### orders.Order
- `id`, `user` FK nullable, `restaurant` FK, `restaurant_name`, `restaurant_logo`
- `subtotal`, `delivery_fee`, `discount`, `tip`, `total` Decimals
- `status` (choices: pending|confirmed|preparing|ready|picked_up|on_the_way|delivered|cancelled)
- `created_at`, `estimated_delivery` DateTime, `delivery_address` text or Address FK
- `payment_method` (string or FK), `courier` JSON, `timeline` JSON or related model
- `external_payment_id` for gateway

### orders.OrderItem (optional normalized)
- `id`, `order` FK, `menu_item_id`, `name`, `quantity`, `price`, `addons` JSON

### orders.OrderTimelineEntry
- `order` FK, `status`, `label`, `time` DateTime/null, `completed` bool

### promotions.Promotion
- `id`, `title`, `description`, `image`, `code` optional, `discount` string, `valid_until` DateTime, `background_color`, `text_color`

### promotions.Coupon
- `id`, `code`, `description`, `discount_type` (percentage|fixed), `discount_value` Decimal
- `minimum_order` Decimal, `valid_until` DateTime, `is_used` Bool, `max_uses` int, `used_count` int, `active` bool

### reviews.Review
- `id`, `user` FK, `user_name`, `user_avatar`, `restaurant` FK, `rating` int, `comment` text, `date` DateTime, `images` JSON

### favorites.Favorite
- `id`, `user` FK, `restaurant` FK, `created_at`

### notifications.Notification
- `id`, `user` FK, `type` (order|promotion|system|review), `title`, `message`, `time`, `is_read`, `action_url`, `icon`

### wallet.Wallet
- `id`, `user` FK unique, `balance` Decimal, `currency`, `promotional_credits` Decimal, `reward_points` int

### wallet.WalletTransaction
- `id`, `wallet` FK, `type` (credit|debit|refund|reward), `description`, `amount`, `date`, `reference`

## API Endpoints (recommended)
Base path: `/api/v1/`

Auth
- `POST /api/v1/auth/register/` — register
- `POST /api/v1/auth/login/` — returns JWT access/refresh
- `POST /api/v1/auth/refresh/`

Users
- `GET/PUT /api/v1/users/me/` — profile
- `GET/POST /api/v1/users/me/addresses/`
- `GET/POST /api/v1/users/me/payment-methods/`

Restaurants & Menu
- `GET /api/v1/restaurants/` — filters: category, featured, trending, open, search
- `GET /api/v1/restaurants/{id}/` — details
- `GET /api/v1/restaurants/{id}/menu/` — menu for a restaurant
- `GET /api/v1/menu-items/{id}/`

Cart
- `GET /api/v1/cart/` — current cart
- `POST /api/v1/cart/items/` — add item (body includes menu_item_id, quantity, selected_addons, instructions)
- `PATCH /api/v1/cart/items/{id}/` — update qty/instructions
- `DELETE /api/v1/cart/items/{id}/`
- `POST /api/v1/cart/apply-coupon/` — validate and apply coupon

Orders
- `POST /api/v1/orders/` — create order (cart snapshot, delivery address, payment method, coupon)
- `GET /api/v1/orders/{id}/` — retrieve
- `GET /api/v1/orders/` — list user's orders
- `POST /api/v1/orders/{id}/cancel/`
- `PATCH /api/v1/orders/{id}/status/` — staff/admin

Promotions & Coupons
- `GET /api/v1/promotions/`
- `POST /api/v1/coupons/validate/` — body: `{ code, subtotal }` → returns `{ valid, discount_amount, new_total }`

Reviews
- `GET /api/v1/restaurants/{id}/reviews/`
- `POST /api/v1/restaurants/{id}/reviews/` — body: `{ rating, comment, images? }`

Favorites
- `GET /api/v1/users/me/favorites/`
- `POST /api/v1/users/me/favorites/` — add
- `DELETE /api/v1/users/me/favorites/{restaurant_id}/` — remove

Notifications
- `GET /api/v1/notifications/`
- `POST /api/v1/notifications/mark-read/` — body: `{ ids: [..] }`

Wallet
- `GET /api/v1/wallet/`
- `GET /api/v1/wallet/transactions/`
- `POST /api/v1/wallet/topup/` — create payment intent

Search
- `GET /api/v1/search/?q=...&type=restaurant|menu`

Dashboard (admin)
- `GET /api/v1/dashboard/stats/` — aggregate metrics

## Request/Response Schemas (examples)

MenuItem (response)
```json
{
  "id": 1,
  "restaurantId": 5,
  "name": "Margherita Pizza",
  "description": "Classic...",
  "price": 9.99,
  "image": "https://...",
  "category": "pizza",
  "available": true,
  "calories": 800,
  "isPopular": true,
  "addons": [{ "id": 1, "name": "Extra Cheese", "price": 1.5 }]
}
```

Order create (request)
```json
{
  "cart_id": "uuid-or-null",
  "items": [{ "menu_item_id": 1, "quantity": 2, "addons": [1], "special_instructions": "no onion" }],
  "delivery_address_id": 3,
  "payment_method_id": 2,
  "coupon_code": "SUMMER10",
  "tip": 1.5
}
```

Order (response)
```json
{
  "id": 123,
  "restaurantId": 5,
  "items": [...],
  "subtotal": 19.98,
  "deliveryFee": 2.5,
  "discount": 2,
  "tip": 1.5,
  "total": 21.98,
  "status": "pending",
  "createdAt": "2026-07-03T12:34:56Z",
  "timeline": [{ "status": "pending", "label": "Order placed", "time": "2026-07-03T12:34:56Z", "completed": true }]
}
```

## Business Rules & Validation
- Re-validate all menu prices and availability server-side at checkout.
- Coupons: check expiry, minimum order, per-user usage, global `max_uses` (atomic decrement in DB transaction).
- Orders: create within DB transaction; create payment intent and store `external_payment_id` before confirming.
- Reviews: only allowed after order delivered (enforce by checking order status and user association).
- Cart: enforce single-restaurant constraint per cart or support multi-restaurant carts with split orders.

## Background tasks & realtime
- Celery (Redis broker) tasks:
  - send order notifications (email/push)
  - process payment webhooks
  - expire promotions and coupons
  - compute dashboard metrics
- Real-time updates:
  - optional Django Channels for websockets (order updates)

## Security & Auth
- Use `djangorestframework-simplejwt` for JWT
- Permissions: `IsAuthenticated` for user endpoints, custom permissions for staff endpoints
- Throttling: DRF throttles for endpoints like auth and coupon validate
- Never store raw card details; use tokenization (Stripe, Paystack)

## DB & Deployment notes
- DB: PostgreSQL (prefer UUID for cart ids)
- Caching: Redis for sessions and rate-limiting
- Storage: S3 for media assets (logos, images)
- Monitoring: Sentry, Prometheus

## Recommended packages
- Django, djangorestframework, djangorestframework-simplejwt
- django-filter, drf-spectacular (OpenAPI), psycopg2-binary
- celery[redis], django-cors-headers, django-storages, boto3

## Next steps
1. Scaffold Django project and apps.
2. Implement models and migrations.
3. Implement serializers + viewsets + routers.
4. Add tests for checkout, coupon usage, wallet transactions.
5. Add Celery tasks and payment gateway integration.

---

## Restaurant and menu routes
GET/POST              /api/v1/restaurants/{restaurant_pk}/addons/
GET/PUT/PATCH/DELETE   /api/v1/restaurants/{restaurant_pk}/addons/{id}/

GET/POST              /api/v1/restaurants/{restaurant_pk}/menu-items/
GET/PUT/PATCH/DELETE   /api/v1/restaurants/{restaurant_pk}/menu-items/{id}/

GET/POST              /api/v1/restaurants/{restaurant_pk}/menu-items/{menuitem_pk}/addon-options/
GET/PUT/PATCH/DELETE   /api/v1/restaurants/{restaurant_pk}/menu-items/{menuitem_pk}/addon-options/{id}/

GET/POST              /api/v1/menu-categories/
GET/PUT/PATCH/DELETE   /api/v1/menu-categories/{id}/

## cart and cartitems routes
GET    /api/v1/cart/                — current cart (creates one if none exists)
POST   /api/v1/cart/apply-coupon/   — placeholder, not yet implemented

GET    /api/v1/cart/items/          — current cart's items
POST   /api/v1/cart/items/          — add an item
PATCH  /api/v1/cart/items/{id}/     — update quantity/instructions
DELETE /api/v1/cart/items/{id}/     — remove an item
