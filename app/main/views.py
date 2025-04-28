from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Category, Product, Cart, Order
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime

# Home page
def home(request):
    return render(request, 'home.html', {})



#search bar
def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query) | Product.objects.filter(tag__icontains=query)
    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'image': product.image.url,
            'tag': product.tag,
        })
    
    return JsonResponse({'products': product_list})

# Best Sellers
def bestsellers(request):
    bestsellers_category = Category.objects.get(name="Best Sellers")
    products = Product.objects.filter(category=bestsellers_category)
    return render(request, 'bestsellers.html', {'products': products})

# New Arrivals
def newarrivals(request):
    new_arrival = Category.objects.get(name="New Arrivals")
    products = Product.objects.filter(category=new_arrival)
    return render(request, 'newarrivals.html', {'products': products})

# Login view
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username does not exist')
            return render(request, 'home.html', {'show_login': True})

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid password')
            return render(request, 'home.html', {'show_login': True})

        login(request, user)
        return redirect('home')

    # For GET requests, show the login modal
    return render(request, 'home.html', {'show_login': True})

# Register view
def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already in use')
            return render(request, 'home.html', {'show_register': True})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        login(request, user)
        return redirect('home')

    # For GET requests, show the register modal
    return render(request, 'home.html', {'show_register': True})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def my_orders(request):
    orders = Order.objects.filter(profile=request.user.profile).order_by('-created_at')  # Newest first
    for order in orders:
        order.created_at_ist = localtime(order.created_at)
    return render(request, 'my_orders.html', {'orders': orders})