from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import Product, Profile
from main.models import Cart, CartItem

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


# def cart_delete(request):
#     cart = Cart(request)
#     if request.POST.get('action') == 'post':
#         product_id = str(request.POST.get('product_id'))  # Ensure it's a string
#         cart.delete(product_id)  # Delete the product from the cart
#         cart.save_session_and_profile()  # Make sure the session and profile are updated
#         return JsonResponse({'status': 'success', 'product_deleted': product_id})
    

# # For updating product quantity in the cart
# def cart_update(request):
#     cart = Cart(request)
#     if request.POST.get('action') == 'post':
#         product_id = request.POST.get('product_id')  # Get the product ID
#         product_qty = request.POST.get('product_qty')  # Get the product quantity
        
#         if product_id and product_qty and product_qty.isdigit():
#             product_id = str(product_id)  # Convert to string
#             product_qty = int(product_qty)  # Convert to integer
            
#             if product_qty <= 0:
#                 return JsonResponse({'error': 'Quantity must be greater than 0.'}, status=400)
            
#             # Call the update method
#             cart.update(product_id, product_qty)  # Update cart with new quantity
            
#             return JsonResponse({'qty': product_qty})  # Return updated quantity
            
#         else:
#             return JsonResponse({'error': 'Invalid product ID or quantity'}, status=400)
        
        

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
