from django.db import migrations
from django.contrib.auth.hashers import make_password

def seed_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    User = apps.get_model('auth', 'User')
    
    # 1. Create a default admin user if none exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            email='admin@luxcart.com',
            password=make_password('AdminPassword123'),
            is_staff=True,
            is_superuser=True
        )
    
    # 2. Seed default categories and products if empty
    if not Category.objects.exists():
        shoes = Category.objects.create(name="Shoes", description="Premium athletic and casual footwear")
        clothing = Category.objects.create(name="Clothing", description="Stylish and comfortable apparel")
        accessories = Category.objects.create(name="Accessories", description="Essential lifestyle accessories")
        
        # Add products
        Product.objects.create(
            category=shoes,
            name="Classic Red Athletic Shoes",
            description="High-performance athletic running shoes with responsive cushioning and breathable mesh.",
            price=89.99,
            image="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=60",
            stock=15
        )
        Product.objects.create(
            category=shoes,
            name="AeroSport Neon Sneakers",
            description="Extremely lightweight and vibrant sneakers designed for everyday walking and light jogging.",
            price=119.99,
            image="https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&auto=format&fit=crop&q=60",
            stock=10
        )
        Product.objects.create(
            category=shoes,
            name="Urban Streetwear High-Tops",
            description="Classic street style high-top sneakers with durable canvas and non-slip rubber soles.",
            price=79.99,
            image="https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=600&auto=format&fit=crop&q=60",
            stock=20
        )
        Product.objects.create(
            category=shoes,
            name="Classic Black Loafers",
            description="Handcrafted genuine leather loafers offering exceptional comfort and sophisticated style.",
            price=149.99,
            image="https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=600&auto=format&fit=crop&q=60",
            stock=8
        )
        Product.objects.create(
            category=clothing,
            name="Premium Cotton T-Shirt",
            description="100% organic long-staple cotton t-shirt with a modern fit and ultra-soft feel.",
            price=29.99,
            image="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=60",
            stock=30
        )
        Product.objects.create(
            category=accessories,
            name="Minimalist Leather Backpack",
            description="Sleek, water-resistant full-grain leather backpack with a padded laptop compartment.",
            price=189.99,
            image="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=60",
            stock=12
        )

def revert_seed_data(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Product = apps.get_model('store', 'Product')
    User = apps.get_model('auth', 'User')
    
    # Only delete the admin we created specifically
    User.objects.filter(username='admin', email='admin@luxcart.com').delete()
    Product.objects.all().delete()
    Category.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_category_order_address_order_city_order_email_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_data, revert_seed_data),
    ]
