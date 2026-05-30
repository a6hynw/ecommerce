# AetherStore 🌌

AetherStore is a modern, premium e-commerce web application built with **Django**. It features a stunning dark-themed glassmorphism UI, a fully functional shopping cart system, and role-based access control with dedicated dashboards for both Store Admins and System Super Admins.

## ✨ Features

### 🛍️ Customer Experience
- **Sleek Authentication**: Split-screen login and registration pages featuring dynamic category displays.
- **Product Browsing**: Beautifully styled product cards with hover effects and detailed product views.
- **Interactive Cart**: AJAX-powered sidebar cart that updates quantities and totals in real-time without page reloads.
- **Seamless Checkout**: A modal-based checkout system for placing orders instantly.
- **Feedback System**: Interactive 5-star CSS rating and feedback form on product pages.

### 🛡️ Admin Portal (Store Managers)
- **Focused Dashboard**: Real-time metrics for Total Products, Pending Orders, and Low Stock Alerts.
- **Product Management**: Full CRUD capabilities to add, edit, or remove products and manage inventory levels.
- **Order Fulfillment**: Track customer orders and update shipping statuses (Pending → Processing → Shipped → Delivered).

### 👑 Super Admin Portal (System Owners)
- **Global Analytics**: High-level metrics for Global Revenue, Active Users, and Total Categories.
- **Real-Time Data Visualization**: An interactive Chart.js graph displaying hourly, monthly, and yearly sales trends.
- **User Directory**: View all registered users and effortlessly promote/revoke Admin privileges or deactivate accounts.
- **Category Control**: Create, edit, and delete store categories dynamically.

---

## 🛠️ Technology Stack
- **Backend**: Python, Django
- **Database**: SQLite (Default)
- **Frontend**: HTML5, Vanilla JavaScript, Vanilla CSS
- **Design System**: Custom CSS variables, Glassmorphism, CSS Grid & Flexbox, Ionicons, Chart.js

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites
Make sure you have Python (3.8+) installed on your machine.

### Installation

1. **Navigate to the project directory**
   Open your terminal and navigate to the `ECommerse` folder.

2. **Create a Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv .venv
   ```
   Activate it:
   - On Windows: `.venv\Scripts\activate`
   - On Mac/Linux: `source .venv/bin/activate`

3. **Install Dependencies**
   Make sure Django is installed:
   ```bash
   pip install django
   ```

4. **Apply Database Migrations**
   Initialize the database schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed the Database (Optional)**
   AetherStore comes with a seed script that automatically creates a Super Admin, an Admin, standard users, categories, and dummy products so you can explore the dashboards immediately.
   ```bash
   python seed.py
   ```
   *Default Seed Credentials:*
   - **Super Admin**: `superadmin` / `SuperadminPass123!`
   - **Admin**: `admin` / `AdminPass123!`
   - **Customer**: `customer` / `CustomerPass123!`

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000` in your browser.

---

## 📁 Project Structure

```text
ECommerse/
├── ecommerce_project/      # Main Django configuration folder
├── shop/                   # Core application
│   ├── models.py           # Database schemas (Product, Order, etc.)
│   ├── views.py            # View logic and role-based access controllers
│   ├── urls.py             # URL routing for the shop
│   ├── context_processors.py # Global context (e.g., cart items)
│   └── templates/shop/     # HTML templates (Dashboards, Auth, Home, etc.)
├── static/
│   └── shop/
│       ├── css/style.css   # The core design system and styling
│       ├── js/main.js      # AJAX cart logic and UI interactions
│       └── images/         # Static visual assets
├── seed.py                 # Database initialization script
└── manage.py               # Django execution script
```

## 🎨 UI/UX Design Notes
AetherStore completely eschews CSS frameworks like Tailwind or Bootstrap in favor of a highly optimized, custom Vanilla CSS architecture. It utilizes a `var(--theme)` root system allowing for cohesive branding using the Deep Dark/Violet palette (`#070F2B`, `#1B1A55`, `#535C91`, `#9290C3`).
