from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_summary, name="cart_summary"),
    path('items/', views.cart_items_api, name='cart_items_api'),
    path('offcanvas/', views.cart_offcanvas, name='cart_offcanvas'),
    path('add/', views.cart_add, name="cart_add"),
    # path('delete/', views.cart_delete, name="cart_delete"),
    # path('update/', views.cart_update, name="cart_update"),
]
