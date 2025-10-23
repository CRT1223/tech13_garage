# TECH13 Garage - Motorcycle Parts & Services Website

A comprehensive web application for TECH13 Garage, specializing in motorcycle parts and services for both racing and daily use.

## Features

### User Interface
- **Homepage**: Featured products, categories, and services showcase
- **Product Catalog**: Browse racing and daily motorcycle parts with filtering
- **Product Details**: Detailed product information with related products
- **Services**: Racing and daily motorcycle services
- **Shopping Cart**: Add products and services to cart
- **Checkout**: Complete order placement with delivery information
- **Order History**: View past orders and their status
- **User Authentication**: Registration and login system

### Admin Interface
- **Dashboard**: Overview of sales, products, customers, and orders
- **Product Management**: Add, edit, and manage motorcycle parts
- **Order Management**: Process and update order status
- **Customer Management**: View and manage customer information
- **Inventory Tracking**: Monitor stock levels and low stock alerts

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons**: Font Awesome
- **Authentication**: Werkzeug password hashing

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tech13_garage
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Admin login: username: `admin`, password: `admin123`

## Database Schema

The application uses SQLite with the following main tables:

- **users**: Customer and admin accounts
- **categories**: Product categories (Engine Parts, Brake Systems, etc.)
- **products**: Motorcycle parts with racing/daily classification
- **services**: Motorcycle services
- **orders**: Customer orders
- **order_items**: Individual items in orders
- **cart**: Shopping cart items
- **reviews**: Product and service reviews

## Key Features

### Product Management
- Categorize products as Racing or Daily use
- Track inventory levels
- Image upload support
- Brand, model, and year range specifications

### Order Processing
- Complete order workflow from cart to delivery
- Order status tracking
- Customer information management
- Order history and details

### Admin Dashboard
- Real-time statistics
- Low stock alerts
- Recent orders overview
- Quick action buttons

## File Structure

```
tech13_garage/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── tech13_garage.db      # SQLite database (created on first run)
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   ├── images/           # Static images
│   └── uploads/          # User uploaded images
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── products.html     # Product catalog
    ├── product_detail.html # Product details
    ├── services.html     # Services page
    ├── cart.html         # Shopping cart
    ├── checkout.html     # Checkout page
    ├── order_history.html # Order history
    ├── order_detail.html # Order details
    └── admin/
        ├── dashboard.html # Admin dashboard
        ├── products.html  # Product management
        ├── add_product.html # Add product form
        ├── orders.html    # Order management
        └── customers.html # Customer management
```

## Usage

### For Customers
1. Register an account or login
2. Browse products by category or type (Racing/Daily)
3. Add items to cart
4. Proceed to checkout
5. Track orders in order history

### For Administrators
1. Login with admin credentials
2. Access admin dashboard for overview
3. Manage products, orders, and customers
4. Monitor inventory levels
5. Update order statuses

## Customization

The application is designed to be easily customizable:

- **Styling**: Modify `static/css/style.css` for custom appearance
- **Functionality**: Update `static/js/main.js` for additional features
- **Database**: Add new tables or fields in `app.py` init_db() function
- **Templates**: Customize HTML templates in the `templates/` directory

## Security Features

- Password hashing using Werkzeug
- Session management
- Input validation
- SQL injection prevention
- File upload restrictions

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile responsive design

## License

This project is created for TECH13 Garage. All rights reserved.

## Support

For technical support or questions, please contact the development team.
