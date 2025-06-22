# Grocery E-commerce App

A Django-based e-commerce application for grocery shopping.

## Features

- Product listing with categories
- Shopping cart functionality
- User authentication
- Checkout process
- Order management
- Responsive design using Bootstrap

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

1. Access the admin interface at `/admin` to add categories and products
2. Browse products on the home page
3. Add items to cart
4. Proceed to checkout
5. Place order

## License

MIT License
