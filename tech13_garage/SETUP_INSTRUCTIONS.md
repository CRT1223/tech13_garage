# TECH13 Garage - Setup Instructions

## Quick Start

### Windows Users
1. Double-click `start.bat` to start the application
2. Open your browser and go to `http://localhost:5000`

### Linux/Mac Users
1. Make the script executable: `chmod +x start.sh`
2. Run: `./start.sh`
3. Open your browser and go to `http://localhost:5000`

## Manual Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   python -c "from app import init_db; init_db()"
   ```

3. **Start Application**
   ```bash
   python app.py
   ```

4. **Access Application**
   - Open browser: `http://localhost:5000`
   - Admin login: username=`admin`, password=`admin123`

## Features Overview

### User Interface
- **Homepage**: Featured products and services
- **Product Catalog**: Browse racing and daily motorcycle parts
- **Services**: Racing and daily motorcycle services
- **Shopping Cart**: Add items and checkout
- **Order Management**: Track orders and history
- **User Profile**: Manage account information

### Admin Interface
- **Dashboard**: Sales statistics and overview
- **Product Management**: Add, edit, manage motorcycle parts
- **Order Management**: Process and track orders
- **Customer Management**: View customer information
- **Inventory Tracking**: Monitor stock levels

## Default Admin Account
- **Username**: admin
- **Password**: admin123

## Sample Data
The application comes with sample data including:
- 8 sample motorcycle parts (racing and daily)
- 8 sample services
- Product categories (Engine Parts, Brake Systems, etc.)

## File Structure
```
tech13_garage/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── start.bat             # Windows startup script
├── start.sh              # Linux/Mac startup script
├── test_app.py           # Test script
├── README.md             # Documentation
├── SETUP_INSTRUCTIONS.md # This file
├── static/               # CSS, JS, images
└── templates/            # HTML templates
```

## Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   - Change port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

2. **Database errors**
   - Delete `tech13_garage.db` and restart the application

3. **Import errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

4. **Permission errors (Linux/Mac)**
   - Make startup script executable: `chmod +x start.sh`

### Testing
Run the test script to verify everything works:
```bash
python test_app.py
```

## Support
For technical support or questions, please refer to the README.md file or contact the development team.

---
**TECH13 Garage** - Motorcycle Parts & Services
