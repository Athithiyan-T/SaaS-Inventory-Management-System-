<div align="center">

# 📦 StockFlow

### A Multi-Tenant SaaS Inventory Management Platform

Built solo, end-to-end — from database schema to deployed cloud infrastructure.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-6B21A8?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Pytest](https://img.shields.io/badge/Tests-22%20passing-3EB489?style=for-the-badge&logo=pytest&logoColor=white)](#testing)

**[🔗 Live Demo](https://saa-s-inventory-management-system-kappa.vercel.app/login)** &nbsp;|&nbsp; **[💻 GitHub Repository](https://github.com/Athithiyan-T/SaaS-Inventory-Management-System-)**

</div>

---

## 👋 What is this?

StockFlow is a **SaaS-style inventory management system** — the kind of internal tool a small retail business, warehouse, or e-commerce seller would use to track what they have in stock, get alerted before they run out, and manage it all through a clean web dashboard.

It's built as a **multi-tenant application**: any number of separate organizations can sign up and use the same platform, with their data kept completely isolated from one another — the same architectural pattern used by real SaaS products like Shopify, Notion, or Linear.

I designed and built the **entire stack myself** — database schema, REST API, authentication, business logic, UI, automated tests, and cloud deployment — to demonstrate full-stack ownership of a product from idea to production.

---

## 🎯 Why this project matters (for recruiters & hiring managers)

If you're short on time, here's the summary:

| What it shows | How |
|---|---|
| **Full-stack capability** | Independently built both a Python/Flask REST API and a React frontend that talk to each other in production |
| **Real-world architecture** | Multi-tenancy, JWT authentication, and password hashing — not just a CRUD toy app |
| **Product thinking** | Built around an actual business need (inventory tracking + low-stock alerts), not just a tech demo |
| **Quality & rigor** | 22 automated backend tests covering auth, data isolation, and business rules |
| **Deployment skills** | Live on Vercel (frontend) + Render with a managed PostgreSQL database (backend) — configured, not just coded |
| **Clean code habits** | Small functions, meaningful names, consistent structure, and a README written for the next person to pick this up |

---
---

## ✨ Features

**Authentication & Multi-Tenancy**
- Sign up automatically creates a new organization + admin user
- Secure password hashing (Werkzeug) — passwords are never stored in plain text
- JWT-based authentication protecting every private route
- All data (products, settings) is strictly scoped to the logged-in user's organization

**Inventory Management**
- Full CRUD on products — name, SKU, description, quantity, cost & selling price
- Duplicate SKU prevention within an organization
- Real-time search by product name or SKU

**Dashboard & Alerts**
- At-a-glance summary: total products, total quantity, low-stock count
- Smart low-stock detection — uses a product's own threshold if set, otherwise falls back to the organization's default
- Configurable default low-stock threshold per organization

**Engineering Quality**
- 22 automated pytest tests (auth, CRUD, data isolation, dashboard math, validation)
- Consistent API response format with proper HTTP status codes
- Input validation with friendly, specific error messages

---

## 🏗️ Tech Stack & Architecture

```
┌─────────────────────┐         REST API (JSON)        ┌──────────────────────┐
│   React + Vite       │ ─────────────────────────────▶ │   Flask + SQLAlchemy  │
│   Tailwind CSS        │ ◀───────────────────────────── │   JWT Auth            │
│   (Vercel)             │        JWT Bearer Token        │   (Render)            │
└─────────────────────┘                                 └──────────┬───────────┘
                                                                     │
                                                                     ▼
                                                          ┌──────────────────────┐
                                                          │   PostgreSQL          │
                                                          │   (Render managed DB) │
                                                          └──────────────────────┘
```

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, React Router, Axios |
| Backend | Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Flask-CORS |
| Database | PostgreSQL (production) / SQLite (local development) |
| Testing | Pytest, isolated in-memory database per test |
| Deployment | Vercel (frontend), Render (backend + managed Postgres) |

---

## 📁 Project Structure

```
stockflow/
├── backend/
│   ├── app.py                  # Flask app factory & entry point
│   ├── config.py               # Environment-aware configuration
│   ├── models/                 # SQLAlchemy models (User, Organization, Product, Settings)
│   ├── routes/                 # API blueprints (auth, products, dashboard, settings)
│   ├── middleware/              # JWT auth helper
│   ├── utils/                   # Validation & response helpers
│   ├── tests/                    # 22 pytest tests
│   ├── render.yaml               # One-click Render deployment blueprint
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/           # Navbar, Sidebar, DashboardCard, ProductTable, ProductForm
│   │   ├── pages/                 # Login, Signup, Dashboard, Products, Settings, etc.
│   │   ├── services/api.js         # Axios client with JWT auto-attachment
│   │   └── App.jsx                  # Routing + protected routes
│   └── package.json
│
└── README.md
```

---

## 🔌 API Reference

**Auth**
| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| POST | `/api/signup` | Create organization + user, returns JWT | ❌ |
| POST | `/api/login` | Authenticate, returns JWT | ❌ |
| POST | `/api/logout` | Confirm logout | ✅ |

**Products**
| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| GET | `/api/products` | List products (`?search=` supported) | ✅ |
| GET | `/api/products/<id>` | Get one product | ✅ |
| POST | `/api/products` | Create a product | ✅ |
| PUT | `/api/products/<id>` | Update a product | ✅ |
| DELETE | `/api/products/<id>` | Delete a product | ✅ |

**Dashboard & Settings**
| Method | Endpoint | Description | Auth |
|---|---|---|:---:|
| GET | `/api/dashboard` | Totals + low-stock list | ✅ |
| GET | `/api/settings` | Get default threshold | ✅ |
| PUT | `/api/settings` | Update default threshold | ✅ |

All protected routes require: `Authorization: Bearer <access_token>`

---


**api tests passing on Postman**, covering:
- Signup/login/logout flows and failure cases (duplicate email, wrong password, missing fields)
- Product CRUD, duplicate SKU rejection, and organization-level data isolation
- Dashboard aggregation math and low-stock threshold logic (product-level vs org default)
- Settings validation (rejects negative thresholds)

Each test runs against a fresh in-memory SQLite database — no shared state, no flaky tests.


## ☁️ Deployment

This project is deployed using a **Vercel + Render** stack:

- **Frontend on Vercel** — root directory `frontend`, env var `VITE_API_URL` pointing at the live backend
- **Backend on Render** — deployed via the included `render.yaml` blueprint, which provisions a free managed **PostgreSQL** database alongside the web service automatically
- **`config.py`** is environment-aware: uses SQLite for local development and switches to Postgres automatically in production via `DATABASE_URL`


---

## 🔮 Future Improvements

- [ ] Refresh tokens + server-side JWT blocklist
- [ ] Role-based access control (Admin vs Staff within an organization)
- [ ] Pagination for large product catalogs
- [ ] CSV import/export for bulk inventory updates
- [ ] Product categories & multi-warehouse support
- [ ] Email alerts when stock runs low
- [ ] Frontend test suite (Vitest + React Testing Library)
- [ ] Audit log of inventory changes

---

## 👤 About the Developer

Built by **Athithiyan T ** — a 2026 ECE graduate transitioning into full-stack and AI engineering, with hands-on experience across Python/Flask, MERN, and applied AI (RAG, LLM integrations).

📫 Full Stack Developer / AI Engineer roles — feel free to connect.
