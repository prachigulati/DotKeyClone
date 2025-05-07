from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import Product, Profile
from main.models import Cart, CartItem, Order
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
import razorpay # type: ignore
from django.conf import settings


@csrf_exempt
@login_required
def cart_add(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty', 1))
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': 'Profile does not exist'})
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': 'Product not found'})
        cart, created = Cart.objects.get_or_create(profile=profile, active=True)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += product_qty
            cart_item.save()
        return JsonResponse({'status': 'success', 'message': 'Item added to cart'})
    return JsonResponse({'status': 'error', 'error': 'Invalid request'})



def cart_items_api(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(profile__user=request.user, active=True).first()
        items = cart.items.select_related('product').all() if cart else []
        data = []
        for item in items:
            data.append({
                'name': item.product.name,
                'image': item.product.image.url,
                'price': item.product.price,
                'quantity': item.quantity,
            })
        return JsonResponse({'items': data})
    else:
        return JsonResponse({'items': []})
    


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_offcanvas(request):
    cart = Cart.objects.filter(profile__user=request.user, active=True).first()
    if cart:
        cart_items = cart.items.select_related('product').all()
        cart_products = [item.product for item in cart_items]
        quantities = {item.product.id: item.quantity for item in cart_items}
        totals = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_products = []
        quantities = {}
        totals = 0
    return render(request, 'offcanvas_cart.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
    })


@csrf_exempt 
def update_cart(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')  
            action = request.POST.get('action')  
            quantity = int(request.POST.get('quantity', 1)) 
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.get(profile__user=request.user, active=True)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            if action == 'add':
                cart_item.quantity += quantity
            elif action == 'subtract':
                cart_item.quantity -= quantity
                if cart_item.quantity <= 0:
                    cart_item.delete()
            elif action == 'remove':
                cart_item.delete()
            cart_item.save()
            return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': 'Product not found'})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': 'Cart not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})
    return JsonResponse({'status': 'error', 'error': 'Invalid request'})




def checkout(request):
    profile = request.user.profile
    try:
        cart = Cart.objects.get(profile=profile, active=True)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    amount_in_paisa = int(total_price * 100)  
    step = request.session.get('checkout_step', 1)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_mobile':
            profile.phone = request.POST.get('mobile_number')
            profile.save()
            request.session['checkout_step'] = 2
            return redirect('cart:checkout')
        elif action == 'save_address':
            profile.address1 = request.POST.get('address1')
            profile.address2 = request.POST.get('address2')
            profile.city = request.POST.get('city')
            profile.state = request.POST.get('state')
            profile.zipcode = request.POST.get('zipcode')
            profile.country = request.POST.get('country')
            profile.save()
            request.session['checkout_step'] = 3
            return redirect('cart:checkout')
        elif action == 'cod':
            if cart:
                order = Order.objects.create(
                    profile=profile,
                    cart=cart,
                    total_price=total_price,
                    payment_method='COD',
                    order_status='Placed',
                )
                cart.active = False
                cart.save()
                request.session.pop('checkout_step', None)
                return redirect('home')  
            else:
                return redirect('cart:checkout')
        elif action == 'go_back':
            request.session['checkout_step'] = 1
            return redirect('cart:checkout')
        elif action == 'go_back_address':
            request.session['checkout_step'] = 2
            return redirect('cart:checkout')
    razorpay_order = None
    if step == 3 and cart_items:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        DATA = {
            "amount": amount_in_paisa,
            "currency": "INR",
            "payment_capture": 1,
        }
        razorpay_order = client.order.create(data=DATA)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'step': step,
        'profile': profile,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'razorpay_order': razorpay_order,
    }
    return render(request, 'checkout.html', context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        profile = request.user.profile
        try:
            cart = Cart.objects.get(profile=profile, active=True)
        except Cart.DoesNotExist:
            return redirect('cart:checkout')
        order = Order.objects.create(
            profile=profile,
            cart=cart,
            total_price=sum(item.product.price * item.quantity for item in cart.items.all()),
            payment_method='Online',
            order_status='Placed',
        )
        cart.active = False
        cart.save()
        request.session.pop('checkout_step', None)
        return redirect('home')
    return redirect('home')



def cart_quantity_api(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(profile__user=request.user, active=True).first()
        total_quantity = sum(item.quantity for item in cart.items.all()) if cart else 0
        return JsonResponse({'quantity': total_quantity})
    return JsonResponse({'quantity': 0})

