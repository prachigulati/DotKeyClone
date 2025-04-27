from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import Product, Profile
from main.models import Cart, CartItem
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

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
        # Get or create active cart for the user
        cart, created = Cart.objects.get_or_create(profile=profile, active=True)
        # Check if the item already exists in the cart
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
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_offcanvas(request):
    # Ensure the cart is filtered by the user through the profile
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
            product_id = request.POST.get('product_id')  # Get the product ID from the form
            action = request.POST.get('action')  # The action (subtract, add, remove)
            quantity = int(request.POST.get('quantity', 1))  # The quantity to add or subtract

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




# def checkout(request):
#     profile = request.user.profile  # get profile of logged-in user
#     try:
#         cart = Cart.objects.get(profile=profile, active=True)  # get active cart
#         cart_items = cart.items.all()  # get all items linked to the cart
#     except Cart.DoesNotExist:
#         cart_items = []  # if no cart, empty list
#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }
#     return render(request, 'checkout.html', context)



# def checkout(request):
#     profile = request.user.profile

#     try:
#         cart = Cart.objects.get(profile=profile, active=True)
#         cart_items = cart.items.all()
#     except Cart.DoesNotExist:
#         cart_items = []

#     total_price = sum(item.product.price * item.quantity for item in cart_items)

#     # Handle form submissions
#     if request.method == 'POST':
#         mobile_number = request.POST.get('mobile_number')

#         if mobile_number:
#             profile.phone = mobile_number
#             profile.save()
#             return redirect('checkout_address')  # Go to address step

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }
#     return render(request, 'checkout.html', context)

def checkout(request):
    profile = request.user.profile

    try:
        cart = Cart.objects.get(profile=profile, active=True)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart_items = []

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Get the current step from session, default to 1
    step = request.session.get('checkout_step', 1)

    if request.method == 'POST':
        action = request.POST.get('action')  # We use "action" value now

        if action == 'save_mobile':
            # Save mobile number
            profile.phone = request.POST.get('mobile_number')
            profile.save()
            request.session['checkout_step'] = 2  # Move to Address Step
            return redirect('cart:checkout')  # Refresh page to show step 2

        elif action == 'save_address':
            # Save address info
            profile.address1 = request.POST.get('address1')
            profile.address2 = request.POST.get('address2')
            profile.city = request.POST.get('city')
            profile.state = request.POST.get('state')
            profile.zipcode = request.POST.get('zipcode')
            profile.country = request.POST.get('country')
            profile.save()
            request.session['checkout_step'] = 1  # Optional: reset step or go to payment
            return redirect('checkout_payment')  # Redirect to payment

        elif action == 'go_back':
            # Go back to mobile number step
            request.session['checkout_step'] = 1
            return redirect('cart:checkout')

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'step': step,
        'profile': profile,
    }
    return render(request, 'checkout.html', context)
