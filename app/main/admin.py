from django.contrib import admin
from .models import Category, Product, Profile, Cart, CartItem, Order
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe


# Register basic models
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)

# Inline profile info with User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

# Extend the default User admin to include Profile
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Unregister the original User admin and register the new one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','profile', 'cart', 'total_price', 'payment_method', 'order_status', 'created_at')
    list_editable = ('order_status',)  
    readonly_fields = ('created_at', 'cart_items_display') 
    list_filter = ('order_status', 'payment_method')
    def cart_items_display(self, obj):
        items = obj.cart.items.all() 
        if not items:
            return "No items"
        html = "<table style='border:1px solid #ccc; border-collapse: collapse;'>"
        html += "<tr><th style='border:1px solid #ccc; padding:5px;'>Product</th><th style='border:1px solid #ccc; padding:5px;'>Quantity</th></tr>"
        for item in items:
            html += f"<tr><td style='border:1px solid #ccc; padding:5px;'>{item.product.name}</td><td style='border:1px solid #ccc; padding:5px;'>{item.quantity}</td></tr>"
        html += "</table>"
        return mark_safe(html)  
    cart_items_display.short_description = "Cart Items" 

admin.site.register(Order, OrderAdmin)