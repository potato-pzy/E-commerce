import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin1').exists():
    User.objects.create_superuser('admin1', 'admin@example.com', 'admin')
    print("Superuser created: admin/admin")
else:
    print("Superuser already exists.")
