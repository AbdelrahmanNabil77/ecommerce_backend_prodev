
# 🛒 E-Commerce Backend API

A robust, scalable backend API for an e-commerce platform built with Django REST Framework. Features include product catalog management, user authentication, advanced filtering, and admin-only content management.

## ✨ Features

-   🔐 **JWT Authentication** - Secure user registration and login
    
-   👑 **Role-Based Access Control** - Admin-only product/category management
    
-   🛍️ **Product Catalog** - Full CRUD operations for products
    
-   📂 **Category Management** - Hierarchical categories and subcategories
    
-   ⭐ **Product Reviews** - User reviews with rating system
    
-   🔍 **Advanced Filtering** - Filter by price, category, stock status, etc.
    
-   📄 **Pagination** - Efficient data handling for large datasets
    
-   📚 **API Documentation** - Interactive Swagger/OpenAPI documentation
    
-   🚀 **Performance Optimized** - Database indexing and query optimization
    

## 🛠️ Technologies

-   **Backend**: Django 4.2, Django REST Framework
    
-   **Database**: PostgreSQL
    
-   **Authentication**: JWT (JSON Web Tokens)
    
-   **Documentation**: Swagger/OpenAPI
    
-   **Filtering**: Django Filter
    
-   **Deployment**: PythonAnywhere (Free Tier)
    

## 📁 Project Structure

text

ecommerce-backend/
├── ecommerce/              # Main project settings
├── users/                  # User authentication app
├── products/               # Products and categories app
├── docs/                   # API documentation
├── manage.py
├── requirements.txt
└── README.md

## 🚀 Quick Start

### Prerequisites

-   Python 3.11+
    
-   PostgreSQL
    
-   Redis (optional, for caching)
    

## 📚 API Documentation

### Interactive Documentation

-   **Swagger UI**: `http://localhost:8000/swagger/`
    
-   **ReDoc**: `http://localhost:8000/redoc/`
    

### API Endpoints Overview

#### 🔐 Authentication

Method

Endpoint

Description

Access

POST

`/api/auth/register/`

User registration

Public

POST

`/api/auth/login/`

User login

Public

POST

`/api/auth/refresh/`

Refresh token

Authenticated

GET

`/api/auth/profile/`

User profile

Authenticated

#### 🛍️ Products

Method

Endpoint

Description

Access

GET

`/api/products/`

List all products

Public

POST

`/api/products/`

Create product

**Admin Only**

GET

`/api/products/{slug}/`

Product details

Public

PUT/PATCH

`/api/products/{slug}/`

Update product

**Admin Only**

DELETE

`/api/products/{slug}/`

Delete product

**Admin Only**

GET

`/api/products/featured/`

Featured products

Public

GET

`/api/products/on_sale/`

Products on sale

Public

#### 📂 Categories

Method

Endpoint

Description

Access

GET

`/api/categories/`

List categories

Public

POST

`/api/categories/`

Create category

**Admin Only**

GET

`/api/categories/{slug}/`

Category details

Public

PUT/PATCH

`/api/categories/{slug}/`

Update category

**Admin Only**

DELETE

`/api/categories/{slug}/`

Delete category

**Admin Only**

#### ⭐ Reviews

Method

Endpoint

Description

Access

GET

`/api/products/{slug}/reviews/`

List product reviews

Public

POST

`/api/products/{slug}/reviews/`

Create review

Authenticated

PUT/PATCH

`/api/products/{slug}/reviews/{id}/`

Update review

**Admin Only**

DELETE

`/api/products/{slug}/reviews/{id}/`

Delete review

**Admin Only**

## 🔧 Advanced Features

### Filtering & Sorting

Products can be filtered and sorted using query parameters:

http

GET /api/products/?min_price=100&max_price=500&category=electronics&ordering=-price

**Available filters:**

-   `category` - Filter by category slug
    
-   `min_price`, `max_price` - Price range
    
-   `featured` - Featured products only
    
-   `in_stock` - Products in stock
    
-   `search` - Search in name, description, SKU
    
-   `ordering` - Sort by `price`, `-price`, `name`, `created_at`, etc.
    

### Pagination

All list endpoints support pagination:

http

GET /api/products/?page=2&page_size=20

Response includes pagination metadata:

json

{
  "links": {
    "next": "...",
    "previous": "..."
  },
  "count": 150,
  "total_pages": 8,
  "current_page": 2,
  "results": [...]
}

### Example API Calls

**Register User:**

bash

curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","first_name":"John","last_name":"Doe"}'

**Login:**

bash

curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

**Create Product (Admin):**

bash

curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"Wireless Headphones","description":"Premium quality","price":199.99,"sku":"WH-1000","quantity":50,"category_id":1}'

## 👥 User Roles & Permissions

### Regular Users

-   ✅ Register and login
    
-   ✅ View products and categories
    
-   ✅ Submit product reviews
    
-   ✅ View own profile
    
-   ❌ Create/update/delete products
    
-   ❌ Create/update/delete categories
    

### Admin Users

-   ✅ All regular user permissions
    
-   ✅ Create/update/delete products
    
-   ✅ Create/update/delete categories
    
-   ✅ Moderate user reviews
    
-   ✅ Access Django admin panel
    

## 🗄️ Database Schema

### Models Overview

1.  **User** - Custom user model with email authentication
    
2.  **Category** - Hierarchical product categories
    
3.  **Product** - Product information with variants
    
4.  **ProductImage** - Product gallery images
    
5.  **ProductReview** - User reviews and ratings
    

### Relationships

-   Category ↔ Product (One-to-Many)
    
-   Product ↔ ProductImage (One-to-Many)
    
-   Product ↔ ProductReview (One-to-Many)
    
-   User ↔ Product (Created by relationship)
    
-   User ↔ ProductReview (Review author)