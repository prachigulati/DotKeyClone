from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('bestsellers/', views.bestsellers, name='bestsellers'), 
    path('newarrivals/', views.newarrivals, name='newarrivals'), 
    path('blog/', views.blog, name='blog'),

    path('blogtemp/post1/', views.post1, name='post1'),
    path('blogtemp/post2/', views.post2, name='post2'),
    path('blogtemp/post3/', views.post3, name='post3'),
    path('blogtemp/post4/', views.post4, name='post4'),
    path('blogtemp/Cpost1/', views.Cpost1, name='Cpost1'),
    path('blogtemp/Cpost2/', views.Cpost2, name='Cpost2'),
    path('blogtemp/Cpost3/', views.Cpost3, name='Cpost3'),
    path('blogtemp/Mpost1/', views.Mpost1, name='Mpost1'),
    path('blogtemp/Rpost1/', views.Rpost1, name='Rpost1'),
    path('blogtemp/Rpost2/', views.Rpost2, name='Rpost2'),
    path('blogtemp/Tpost1/', views.Tpost1, name='Tpost1'),
    path('blogtemp/Tpost2/', views.Tpost2, name='Tpost2'),
    path('blogtemp/Spost1/', views.Spost1, name='Spost1'),
    path('blogtemp/Spost2/', views.Spost2, name='Spost2'),
    path('blogtemp/Spost3/', views.Spost3, name='Spost3'),
    path('blogtemp/Spost4/', views.Spost4, name='Spost4'),

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
