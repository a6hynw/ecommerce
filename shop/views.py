from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDate, TruncHour, TruncMonth
from django.views.decorators.http import require_POST
import json
from decimal import Decimal
from django.utils import timezone
import calendar

from .models import Category, Product, CartItem, Order, OrderItem

# Role Check Decorators
def admin_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),
        login_url='login'
    )
    return actual_decorator(view_func)

def superadmin_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url='login'
    )
    return actual_decorator(view_func)

# --- AUTHENTICATION MODULE ---

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'shop/register.html', {'categories': categories})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'shop/register.html', {'categories': categories})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f"Welcome, {username}! Registration successful.")
        return redirect('home')
    return render(request, 'shop/register.html', {'categories': categories})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            # Redirect based on role
            if user.is_superuser:
                return redirect('super_admin_dashboard')
            elif user.is_staff:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'shop/login.html', {'categories': categories})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# --- USER MODULE (CUSTOMER) ---

@login_required
def home_view(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    products = Product.objects.all()

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Sort
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
        'sort_by': sort_by,
    }
    return render(request, 'shop/home.html', context)

@login_required
def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # Simple recommendation: other products in same category
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)

@login_required
@require_POST
def cart_add_view(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    product = get_object_or_404(Product, id=product_id)
    
    if product.stock < quantity:
        return JsonResponse({'error': f'Only {product.stock} items left in stock'}, status=400)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        if product.stock < cart_item.quantity + quantity:
            return JsonResponse({'error': f'Cannot add more. Only {product.stock} items in stock.'}, status=400)
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    
    total_qty = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    return JsonResponse({'success': True, 'message': 'Product added to cart', 'cart_count': total_qty})

@login_required
@require_POST
def cart_update_view(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity'))
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    if quantity <= 0:
        return JsonResponse({'error': 'Quantity must be at least 1'}, status=400)

    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if cart_item.product.stock < quantity:
        return JsonResponse({'error': f'Only {cart_item.product.stock} items in stock'}, status=400)

    cart_item.quantity = quantity
    cart_item.save()

    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.subtotal for item in cart_items)
    item_subtotal = cart_item.subtotal
    total_qty = cart_items.aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        'success': True,
        'item_subtotal': float(item_subtotal),
        'cart_total': float(cart_total),
        'cart_count': total_qty
    })

@login_required
@require_POST
def cart_remove_view(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()

    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.subtotal for item in cart_items)
    total_qty = cart_items.aggregate(total=Sum('quantity'))['total'] or 0

    return JsonResponse({
        'success': True,
        'cart_total': float(cart_total),
        'cart_count': total_qty
    })

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('home')

    total = sum(item.subtotal for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        shipping_address = request.POST.get('shipping_address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')

        # Double check stock
        for item in cart_items:
            if item.product.stock < item.quantity:
                messages.error(request, f"Sorry, {item.product.name} is now out of stock or does not have enough quantity.")
                return redirect('cart')

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            shipping_address=shipping_address,
            city=city,
            zip_code=zip_code,
            total_price=total,
            status='Pending'
        )

        # Create OrderItems & deplete stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            # Deplete stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear cart
        cart_items.delete()
        messages.success(request, f"Order placed successfully! Order #{order.id} is being processed.")
        return redirect('dashboard')

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'shop/dashboard.html', context)


# --- ADMIN MODULE ---

@admin_required
def admin_dashboard_view(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    orders = Order.objects.all().order_by('-created_at')
    
    # Simple statistics
    total_products = Product.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    low_stock_products = Product.objects.filter(stock__lte=5).count()

    context = {
        'products': products,
        'categories': categories,
        'orders': orders,
        'total_products': total_products,
        'pending_orders': pending_orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'shop/admin_dashboard.html', context)

@admin_required
@require_POST
def admin_add_product(request):
    name = request.POST.get('name')
    category_id = request.POST.get('category')
    description = request.POST.get('description')
    price = request.POST.get('price')
    stock = request.POST.get('stock')
    image_url = request.POST.get('image_url')

    category = get_object_or_404(Category, id=category_id)
    Product.objects.create(
        name=name,
        category=category,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url
    )
    messages.success(request, f"Product '{name}' added successfully!")
    return redirect('admin_dashboard')

@admin_required
@require_POST
def admin_edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.name = request.POST.get('name')
    category_id = request.POST.get('category')
    product.category = get_object_or_404(Category, id=category_id)
    product.description = request.POST.get('description')
    product.price = Decimal(request.POST.get('price'))
    product.stock = int(request.POST.get('stock'))
    product.image_url = request.POST.get('image_url')
    product.save()

    messages.success(request, f"Product '{product.name}' updated successfully!")
    return redirect('admin_dashboard')

@admin_required
@require_POST
def admin_delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    name = product.name
    product.delete()
    messages.success(request, f"Product '{name}' was deleted.")
    return redirect('admin_dashboard')

@admin_required
@require_POST
def admin_update_order_status(request, id):
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    if status in dict(Order.STATUS_CHOICES):
        order.status = status
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {status}.")
    else:
        messages.error(request, "Invalid status choice.")
    return redirect('admin_dashboard')


# --- SUPER ADMIN MODULE ---

@superadmin_required
def super_admin_dashboard_view(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    users = User.objects.all().order_by('-date_joined')

    # Total numbers
    total_revenue = Order.objects.exclude(status='Cancelled').aggregate(sum=Sum('total_price'))['sum'] or Decimal('0.00')
    active_users = User.objects.count()
    total_categories = Category.objects.count()

    # --- Time Aggregations for Chart ---
    now = timezone.now()
    
    # 1. Daily (24 hours)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    hourly_sales = (
        Order.objects.filter(created_at__gte=today_start).exclude(status='Cancelled')
        .annotate(hour=TruncHour('created_at'))
        .values('hour')
        .annotate(total=Sum('total_price'))
        .order_by('hour')
    )
    daily_labels = [f"{i:02d}:00" for i in range(24)]
    daily_values = [0.0] * 24
    for s in hourly_sales:
        if s['hour']:
            hr = timezone.localtime(s['hour']).hour if timezone.is_aware(s['hour']) else s['hour'].hour
            daily_values[hr] = float(s['total'])

    # 2. Monthly (Current Month)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    daily_sales_this_month = (
        Order.objects.filter(created_at__gte=month_start).exclude(status='Cancelled')
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('total_price'))
        .order_by('day')
    )
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    monthly_labels = [f"Day {i}" for i in range(1, days_in_month + 1)]
    monthly_values = [0.0] * days_in_month
    for s in daily_sales_this_month:
        if s['day']:
            day_idx = s['day'].day - 1
            monthly_values[day_idx] = float(s['total'])

    # 3. Yearly (Current Year)
    year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_sales_this_year = (
        Order.objects.filter(created_at__gte=year_start).exclude(status='Cancelled')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total_price'))
        .order_by('month')
    )
    yearly_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    yearly_values = [0.0] * 12
    for s in monthly_sales_this_year:
        if s['month']:
            month_idx = s['month'].month - 1
            yearly_values[month_idx] = float(s['total'])

    chart_data = {
        'daily': {'labels': daily_labels, 'values': daily_values},
        'monthly': {'labels': monthly_labels, 'values': monthly_values},
        'yearly': {'labels': yearly_labels, 'values': yearly_values},
    }

    context = {
        'categories': categories,
        'users': users,
        'total_revenue': total_revenue,
        'active_users': active_users,
        'total_categories': total_categories,
        'chart_data_json': json.dumps(chart_data),
    }
    return render(request, 'shop/super_admin_dashboard.html', context)

@superadmin_required
@require_POST
def super_add_category(request):
    name = request.POST.get('name')
    description = request.POST.get('description', '')
    if name:
        Category.objects.create(name=name, description=description)
        messages.success(request, f"Category '{name}' created successfully.")
    else:
        messages.error(request, "Category name cannot be empty.")
    return redirect('super_admin_dashboard')

@superadmin_required
@require_POST
def super_edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.name = request.POST.get('name')
    category.description = request.POST.get('description', '')
    category.save()
    messages.success(request, f"Category '{category.name}' updated successfully.")
    return redirect('super_admin_dashboard')

@superadmin_required
@require_POST
def super_delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    name = category.name
    category.delete()
    messages.success(request, f"Category '{name}' deleted successfully.")
    return redirect('super_admin_dashboard')

@superadmin_required
@require_POST
def super_manage_user_role(request, id):
    user = get_object_or_404(User, id=id)
    role_action = request.POST.get('role_action')

    # Guard against demoting self
    if user == request.user:
        messages.error(request, "You cannot alter your own permissions.")
        return redirect('super_admin_dashboard')

    if role_action == 'make_admin':
        user.is_staff = True
        user.save()
        messages.success(request, f"User {user.username} has been promoted to Admin.")
    elif role_action == 'remove_admin':
        user.is_staff = False
        user.is_superuser = False
        user.save()
        messages.success(request, f"Admin privileges revoked for {user.username}.")
    elif role_action == 'make_superadmin':
        user.is_staff = True
        user.is_superuser = True
        user.save()
        messages.success(request, f"User {user.username} has been promoted to Super Admin.")
    elif role_action == 'deactivate':
        user.is_active = False
        user.save()
        messages.success(request, f"User {user.username} account has been deactivated.")
    elif role_action == 'activate':
        user.is_active = True
        user.save()
        messages.success(request, f"User {user.username} account has been reactivated.")
        
    return redirect('super_admin_dashboard')
