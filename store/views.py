from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Profile, Cart, CartItem, Order, OrderItem
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, CheckoutForm

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
        return cart

def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    products = Product.objects.all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
    if category_id:
        products = products.filter(category_id=category_id)
        
    categories = Category.objects.all()
    
    # Get cart items count to show in navbar
    cart = _get_or_create_cart(request)
    cart_count = cart.items_count if cart else 0
    
    return render(request, "index.html", {
        "products": products,
        "categories": categories,
        "query": query,
        "selected_category": int(category_id) if category_id.isdigit() else None,
        "cart_count": cart_count
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)
    cart_count = cart.items_count if cart else 0
    
    return render(request, "product_detail.html", {
        "product": product,
        "cart_count": cart_count
    })

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            
            # Merge session cart into user cart if exists
            session_key = request.session.session_key
            if session_key:
                try:
                    session_cart = Cart.objects.get(session_id=session_key)
                    user_cart, created = Cart.objects.get_or_create(user=user)
                    for item in session_cart.items.all():
                        user_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                        if not item_created:
                            user_item.quantity += item.quantity
                        else:
                            user_item.quantity = item.quantity
                        user_item.save()
                    session_cart.delete()
                except Cart.DoesNotExist:
                    pass
                    
            messages.success(request, "Registration successful! Welcome to our store.")
            return redirect("/")
        else:
            messages.error(request, "Registration failed. Please check the details and try again.")
    else:
        form = RegisterForm()
        
    return render(request, "register.html", {
        "form": form,
        "cart_count": 0
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Merge session cart into user cart if exists
            session_key = request.session.session_key
            if session_key:
                try:
                    session_cart = Cart.objects.get(session_id=session_key)
                    user_cart, created = Cart.objects.get_or_create(user=user)
                    for item in session_cart.items.all():
                        user_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                        if not item_created:
                            user_item.quantity += item.quantity
                        else:
                            user_item.quantity = item.quantity
                        user_item.save()
                    session_cart.delete()
                except Cart.DoesNotExist:
                    pass
                    
            messages.success(request, f"Welcome back, {user.username}!")
            # Check for next parameter
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, "login.html", {
        "form": form,
        "cart_count": 0
    })

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("/")

@login_required(login_url='login')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        
    cart = _get_or_create_cart(request)
    cart_count = cart.items_count if cart else 0
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'cart_count': cart_count
    })

def cart_detail(request):
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all() if cart else []
    
    return render(request, "cart.html", {
        "cart": cart,
        "cart_items": cart_items,
        "cart_count": cart.items_count if cart else 0
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check stock
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect('product_detail', product_id=product.id)
        
    cart = _get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Updated quantity of {product.name} in your cart.")
        else:
            messages.warning(request, f"Cannot add more of {product.name}. Only {product.stock} items in stock.")
    else:
        cart_item.quantity = 1
        cart_item.save()
        messages.success(request, f"Added {product.name} to your cart.")
        
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"Removed {product_name} from your cart.")
    return redirect('cart')

def update_cart_quantity(request, item_id, action):
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    if action == 'increase':
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, f"Cannot add more. Only {cart_item.product.stock} items in stock.")
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.name} from your cart.")
            
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    cart = _get_or_create_cart(request)
    if not cart or cart.items_count == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')
        
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = cart.total_price
            order.save()
            
            # Create order items and adjust stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                # Deduct stock
                item.product.stock -= item.quantity
                item.product.save()
                
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, "Thank you for your order! Your order has been placed successfully.")
            return redirect('orders')
        else:
            messages.error(request, "Please check the delivery details entered.")
    else:
        # Pre-fill checkout details from profile
        initial_data = {
            'customer': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
            'phone': profile.phone,
            'address': profile.address,
            'city': profile.city,
            'zip_code': profile.zip_code
        }
        form = CheckoutForm(initial=initial_data)
        
    return render(request, "checkout.html", {
        "form": form,
        "cart": cart,
        "cart_count": cart.items_count
    })

@login_required(login_url='login')
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    cart = _get_or_create_cart(request)
    cart_count = cart.items_count if cart else 0
    
    return render(request, "orders.html", {
        "orders": orders,
        "cart_count": cart_count
    })