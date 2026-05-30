# import os
# import django

# # Setup Django Environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
# django.setup()

# from django.contrib.auth.models import User
# from shop.models import Category, Product

# def seed_db():
#     print("Starting database seeding...")

#     # 1. Create Users
#     print("Creating users...")
    
#     # Super Admin
#     if not User.objects.filter(username='superadmin').exists():
#         super_user = User.objects.create_superuser(
#             username='superadmin',
#             email='superadmin@aetherstore.com',
#             password='SuperadminPass123!'
#         )
#         print("Created Super Admin user 'superadmin' / 'SuperadminPass123!'")
#     else:
#         print("Super Admin 'superadmin' already exists.")

#     # Admin
#     if not User.objects.filter(username='admin').exists():
#         admin_user = User.objects.create_user(
#             username='admin',
#             email='admin@aetherstore.com',
#             password='AdminPass123!'
#         )
#         admin_user.is_staff = True
#         admin_user.save()
#         print("Created Admin user 'admin' / 'AdminPass123!'")
#     else:
#         print("Admin 'admin' already exists.")

#     # Standard Customer
#     if not User.objects.filter(username='customer').exists():
#         customer_user = User.objects.create_user(
#             username='customer',
#             email='customer@aetherstore.com',
#             password='CustomerPass123!'
#         )
#         print("Created Customer user 'customer' / 'CustomerPass123!'")
#     else:
#         print("Customer 'customer' already exists.")

#     # 2. Create Categories
#     print("Creating categories...")
#     keyboards_cat, _ = Category.objects.get_or_create(
#         name="Mechanical Keyboards",
#         description="Tactile, clicky, and hot-swappable premium keyboards."
#     )
#     mats_cat, _ = Category.objects.get_or_create(
#         name="Desk Mats",
#         description="Premium felt and stitched custom desk protectors."
#     )
#     accessories_cat, _ = Category.objects.get_or_create(
#         name="Tech Accessories",
#         description="Minimalist charging docks, cord organizers, and office widgets."
#     )

#     # 3. Create Products
#     print("Creating products...")
    
#     # Keyboard 1
#     Product.objects.get_or_create(
#         name="Aether Apex 75%",
#         category=keyboards_cat,
#         defaults={
#             'description': "Compact 75% mechanical typing layout. Features lubed custom POM switches, solid aluminum frame, noise-dampening foam, and a retro grey keycap scheme.",
#             'price': 169.99,
#             'stock': 12,
#             'image_url': "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=600&q=80"
#         }
#     )
    
#     # Keyboard 2
#     Product.objects.get_or_create(
#         name="Vortex Click Pro",
#         category=keyboards_cat,
#         defaults={
#             'description': "Full-sized clicky masterpiece with cherry blue equivalent tactile click switches, hot-swappable sockets, and premium RGB custom backlighting.",
#             'price': 119.50,
#             'stock': 4, # Low stock alert trigger
#             'image_url': "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=600&q=80"
#         }
#     )

#     # Desk Mat
#     Product.objects.get_or_create(
#         name="Sleek Slate Wool Desk Mat",
#         category=mats_cat,
#         defaults={
#             'description': "Handcrafted 100% Merino wool felt desk pad. Protects your desk, dampens acoustic resonance from keystrokes, and provides a cozy work surface.",
#             'price': 45.00,
#             'stock': 20,
#             'image_url': "https://images.unsplash.com/photo-1632292224971-0d45778b3002?auto=format&fit=crop&w=600&q=80"
#         }
#     )

#     # Charger
#     Product.objects.get_or_create(
#         name="Carbon MagSafe Stand",
#         category=accessories_cat,
#         defaults={
#             'description': "Magnetic fast-charging phone stand built with aerospace carbon fiber and weighted walnut base. Zero desktop slipping.",
#             'price': 59.99,
#             'stock': 2, # Low stock alert trigger
#             'image_url': "https://images.unsplash.com/photo-1622445262465-2481c4574875?auto=format&fit=crop&w=600&q=80"
#         }
#     )

#     # Organizer
#     Product.objects.get_or_create(
#         name="Walnut Cable Block",
#         category=accessories_cat,
#         defaults={
#             'description': "Keep your charger and auxiliary cables aligned. Heavy solid walnut block containing three magnetic slots to keep cords at hand.",
#             'price': 19.99,
#             'stock': 35,
#             'image_url': "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?auto=format&fit=crop&w=600&q=80"
#         }
#     )

#     print("Database seeding completed successfully!")

# if __name__ == '__main__':
#     seed_db()
