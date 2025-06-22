import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='seller').exists():
    User.objects.create_superuser('seller', 'admin@example.com', 'admin')
    print("Superuser created: seller/admin")
else:
    print("Superuser already exists.")
