from django.contrib import admin
from .models import Category, Product, Profile, Cart, CartItem
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
