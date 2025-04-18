import json
from django.shortcuts import get_object_or_404
from main.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    # def db_add(self, product, quantity):
    #     product_id = str(product)
    #     product_qty = str(quantity)
        
    #     # Add product to cart
    #     if product_id not in self.cart:
    #         self.cart[product_id] = int(product_qty)
    #     self.session.modified = True

    #     # If user is authenticated, update their profile's cart
    #     if self.request.user.is_authenticated:
    #         current_user, created = Profile.objects.get_or_create(user=self.request.user)
    #         cart_str = str(self.cart).replace("'", "\"")
    #         current_user.old_cart = cart_str
    #         current_user.save()

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        # Add product to cart
        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # If user is authenticated, update their profile's cart
        if self.request.user.is_authenticated:
            current_user, created = Profile.objects.get_or_create(user=self.request.user)
            cart_str = str(self.cart).replace("'", "\"")
            current_user.old_cart = cart_str
            current_user.save()

    def __len__(self):
        return sum(self.cart.values())  # Sum of all item quantities in the cart

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)
        return total

    def get_total_quantity(self):
        return sum(self.cart.values())

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        return self.cart

    # def update(self, product, quantity):
    #     product_id = str(product)
    #     product_qty = int(quantity)
    #     self.cart[product_id] = product_qty
    #     self.session.modified = True

    #     if self.request.user.is_authenticated:
    #         current_user, created = Profile.objects.get_or_create(user=self.request.user)
    #         cart_str = str(self.cart).replace("'", "\"")
    #         current_user.old_cart = cart_str
    #         current_user.save()

    #     return self.cart
    
    # def delete(self, product_id):
    #     product_id = str(product_id)  
    #     if product_id in self.cart:
    #         del self.cart[product_id]
    #         self.save()