from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, RegisteredUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import RegisteredUser
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
import boto3
import csv
import io
from .s3_reader import fetch_products_from_s3


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            hashed_password = make_password(password)  # Encrypt password
            user = RegisteredUser(username=username, email=email, password=hashed_password)
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")
        except IntegrityError:
            messages.error(request, "Username or Email already exists!")

    return render(request, "account/register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = RegisteredUser.objects.filter(username=username).first()

        if user and check_password(password, user.password):  # Check hashed password
            request.session["user_id"] = user.id  # Store user in session
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("home")  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "account/login.html")


########################### User Logout
def user_logout(request):
    logout(request)
    return render(request, "account/logout.html")

"""def search_results(request):
    query = request.GET.get('q', '').strip().lower()
    products = []
    error_message = None

    try:
        all_products = fetch_products_from_s3()  # Get products from S3 + metadata
        if query:
            products = [
                product for product in all_products
                if query in product['name'].lower()
            ]
            if not products:
                error_message = "Product not available"
        else:
            error_message = "Please enter a search term."
    except Exception as e:
        error_message = f"Error fetching data: {str(e)}"

    return render(request, 'store/product_list.html', {
        'products': products,
        'query': query,
        'error_message': error_message
    })"""

def search_results(request):
    query = request.GET.get('q', '').strip().lower()
    products = []
    error_message = "Item not avalibale" # Don't set the message unless needed

    if query:
        all_products = fetch_products_from_s3()  # Your S3 product source
        products = [p for p in all_products if query in p['name'].lower()]

        if not products:
            error_message = f"No products found for '{query}' 💔"

    return render(request, 'store/search_results.html', {
        'products': products,
        'query': query,
        'error_message': error_message
    })
def home_view(request):
    product_images = fetch_products_from_s3()
    return render(request, 'store/home.html', {'product_images': product_images})

def account_page(request):
    return render(request, 'account/account.html')

def about_view(request):
    return render(request,"account/about.html")
@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        image = request.POST.get('product_image')
        description = request.POST.get('product_description')

        cart = request.session.get('cart', {})

        key = f"{name}-{price}"  # or any unique ID
        if key in cart:
            cart[key]['quantity'] += 1
        else:
            cart[key] = {
                'name': name,
                'price': float(price),
                'image': image,
                'description': description,
                'quantity': 1,
                'key': key,
            }

        request.session['cart'] = cart

        return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for key, item in cart.items():
        if item['quantity'] > 0:  # ✅ Only show non-zero items
            item_total = float(item['price']) * item['quantity']
            item['total_price'] = f"{item_total:.2f}"
            item['key'] = key
            cart_items.append(item)
            total_price += item_total

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': f"{total_price:.2f}"
    })

@csrf_exempt
def remove_from_cart(request):
    if request.method == "POST":
        key = request.POST.get('item_key')
        cart = request.session.get('cart', {})

        if key and key in cart:
            cart[key]['quantity'] = 0
            request.session['cart'] = cart

    return redirect('cart')


@csrf_exempt
def update_cart_quantity(request):
    if request.method == "POST":
        key = request.POST.get('item_key')
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity < 1:
                quantity = 1
        except (TypeError, ValueError):
            quantity = 1

        cart = request.session.get('cart', {})

        if key and key in cart:
            cart[key]['quantity'] = quantity
            request.session['cart'] = cart

    return redirect('cart')

def checkout_view(request):
    return render(request, 'store/checkout.html')

def purchases(request):
    # cart logic
    return render(request, 'store/purchases.html')


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
    })
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})















