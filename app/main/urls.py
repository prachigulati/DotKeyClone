from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('bestsellers/', views.bestsellers, name='bestsellers'), 
    path('newarrivals/', views.newarrivals, name='newarrivals'), 
    path('login/', views.login_page, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_products, name='search_products'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('track-order/', views.track_order, name='track_order'),
    path('products/search/', views.product_search, name='product_search'),
    path('products/searchtype/', views.product_type_search, name='product_type_search'),
    path('shopall/', views.shopall, name='shopall'),
]
