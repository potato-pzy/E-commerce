from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q

# Create your views here.

from .models import Product, Category, Cart, CartItem, Order, Review, OrderItem
from .forms import CustomUserCreationForm
from django.db import models

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            review, created = Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={'rating': rating, 'comment': comment}
            )
            if created:
                messages.success(request, 'Review added successfully!')
            else:
                messages.success(request, 'Review updated successfully!')
            return redirect('product_detail', product_id=product_id)
        
    avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
        'avg_rating': round(avg_rating, 1) if avg_rating else None
    })

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    
    # Filter by search query
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    # Filter by category
    if category_id:
        products = products.filter(category_id=category_id)
        
    # Get active category for highlighting in template
    active_category = None
    if category_id:
        active_category = get_object_or_404(Category, id=category_id)

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'active_category': active_category
    })

# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to cart!")
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('cart')

# @login_required
# def checkout(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     if request.method == 'POST':
#         order = Order.objects.create(
#             user=request.user,
#             address=request.POST.get('address'),
#             phone=request.POST.get('phone'),
#             total_amount=cart.get_total()
#         )
#         cart.cartitem_set.all().delete()
#         messages.success(request, "Order placed successfully!")
#         # If the app's URLs are namespaced, include the namespace in reverse
#         return redirect(reverse('order_confirmation', kwargs={'order_id': order.id})
# )
    
#     return render(request, 'store/checkout.html', {'cart': cart})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        # Create the order
        order = Order.objects.create(
            user=request.user,
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_amount=cart.get_total()
        )
        
        # Create order items from cart items
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price  # Store current price
            )
        
        # Clear the cart
        cart.cartitem_set.all().delete()
        messages.success(request, "Order placed successfully!")
        return redirect(reverse('order_confirmation', kwargs={'order_id': order.id}))
    
    return render(request, 'store/checkout.html', {'cart': cart})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to our store.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'store/signup.html', {'form': form})
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            # Redirect to next parameter if it exists
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'store/login.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})