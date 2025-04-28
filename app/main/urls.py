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
]