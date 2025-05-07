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

#blog page
def blog(request):
    return render(request, 'blog.html', {})

def post1(request):
    return render(request, 'blogtemp/post1.html', {})
def post2(request):
    return render(request, 'blogtemp/post2.html', {})
def post3(request):
    return render(request, 'blogtemp/post3.html', {})
def post4(request):
    return render(request, 'blogtemp/post4.html', {})
def Cpost1(request):
    return render(request, 'blogtemp/Cpost1.html', {})
def Cpost2(request):
    return render(request, 'blogtemp/Cpost2.html', {})
def Cpost3(request):
    return render(request, 'blogtemp/Cpost3.html', {})
def Mpost1(request):
    return render(request, 'blogtemp/Mpost1.html', {})
def Rpost1(request):
    return render(request, 'blogtemp/Rpost1.html', {})
def Rpost2(request):
    return render(request, 'blogtemp/Rpost2.html', {})
def Spost1(request):
    return render(request, 'blogtemp/Spost1.html', {})
def Spost2(request):
    return render(request, 'blogtemp/Spost2.html', {})
def Spost3(request):
    return render(request, 'blogtemp/Spost3.html', {})
def Spost4(request):
    return render(request, 'blogtemp/Spost4.html', {})
def Tpost1(request):
    return render(request, 'blogtemp/Tpost1.html', {})
def Tpost2(request):
    return render(request, 'blogtemp/Tpost2.html', {})




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


def track_order(request):
    order = None
    error_message = None

    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        mobile = request.POST.get('mobile')

        try:
            order = Order.objects.get(order_number=order_number)
            if str(order.profile.phone) != str(mobile):  # <- Corrected here
                error_message = "Mobile number does not match with the order."
                order = None  # Hide details if mobile doesn't match
        except Order.DoesNotExist:
            error_message = "No order found with that number."

    return render(request, 'track_order.html', {'order': order, 'error_message': error_message})


import re 

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def product_search(request):
    keywords = request.GET.getlist('q')
    products = Product.objects.all()
    if keywords:
        from django.db.models import Q
        query = Q()
        for word in keywords:
            query |= Q(name__icontains=word)
        products = products.filter(query)
        # Just use the first keyword for banner image
        banner_slug = slugify(keywords[0])
    else:
        banner_slug = 'default'
    return render(request, 'search.html', {
        'products': products,
        'filter': keywords,
        'banner_image': f'assets/{banner_slug}.jpg'
    })



def product_type_search(request):
    keywords = request.GET.getlist('q')
    products = Product.objects.all()
    if keywords:
        from django.db.models import Q
        query = Q()
        for word in keywords:
            query |= Q(description__icontains=word)
        products = products.filter(query)
        # Just use the first keyword for banner image
        banner_slug = slugify(keywords[0])
    else:
        banner_slug = 'default'
    return render(request, 'search.html', {
        'products': products,
        'filter': keywords,
        'banner_image': f'assets/{banner_slug}.jpg'
    })



def shopall(request):
    products = Product.objects.all()
    return render(request, 'shopall.html', {'products': products})
