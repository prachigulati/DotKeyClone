from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    # old_cart = models.CharField(max_length=200, blank=True, null=True)
    old_cart = models.TextField(blank=True, null=True, default='{}')
    def __str__(self):
        return self.user.username
    
#create a user profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

#automate the profile thing
post_save.connect(create_profile, sender=User)



#Categories of product
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name



#Products
class Product(models.Model):
    name =  models.CharField(max_length=100)
    price =  models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category =  models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description =  models.CharField(max_length=250,default=' ',blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    tag=models.CharField(max_length=50)
    # type=models.CharField(max_length=50)
    rating=models.DecimalField(default=0,decimal_places=2,max_digits=6)
    rating_next=models.DecimalField(default=0,decimal_places=2,max_digits=6)
    weight=models.CharField(max_length=50)
    #add sale
    is_sale = models.BooleanField(default=False)
    sale_percentage = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    def __str__(self):
        return self.name

class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
