from django.urls import path
from .views import product_list, product_detail, category_products, user_login, register, user_logout, account_page, \
    cart_view, purchases, home_view, search_results, add_to_cart,about_view, remove_from_cart, update_cart_quantity, checkout_view

urlpatterns = [
    path('home_view/', home_view, name='home'),
    path('product_list', product_list, name='product_list'),
    path('product', product_detail, name='product_detail'),
    path('category', category_products, name='category_products'),
    path('', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('account/', account_page, name='account'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/', update_cart_quantity, name='update_cart_quantity'),
    path('checkout/',checkout_view, name='checkout'),
    path('cart/', cart_view, name='cart'),
    path('purchases/', purchases, name='purchases'),
    path('search/', search_results, name='search_results'),
    path('about/', about_view, name='about'),


    ]

