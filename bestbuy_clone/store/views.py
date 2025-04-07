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
from django.conf import settings



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
    return redirect('login')



def search_results(request):
    query = request.GET.get('q', '').strip().lower()
    products = []
    error_message = None

    if query:
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id='AKIAVRUVRMXJ324MOBGS',
                aws_secret_access_key='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',
                region_name='us-east-1'
            )
            obj = s3.get_object(Bucket='product999', Key='products11.csv')
            csv_data = obj['Body'].read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(csv_data))

            for row in reader:
                if query in row['name'].lower():
                    products.append(row)

            if not products:
                error_message = "Product not available"

        except Exception as e:
            error_message = f"Error fetching data: {str(e)}"

    return render(request, 'store/search_results.html', {
        'products': products,
        'query': query,
        'error_message': error_message
    })


def home_view(request):
    return render(request, 'store/home.html')

def account_page(request):
    return render(request, 'account/account.html')


def add_to_cart(request):
    if request.method == "POST":
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        image = request.POST.get('product_image')
        description = request.POST.get('product_description')

        # Create a unique key using name+price
        key = f"{name}-{price}"

        cart = request.session.get('cart', {})

        if key in cart:
            cart[key]['quantity'] += 1
        else:
            cart[key] = {
                'name': name,
                'price': price,
                'image': image,
                'description': description,
                'quantity': 1
            }

        request.session['cart'] = cart
        return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = list(cart.values())  # Get product info directly

    return render(request, 'store/cart.html', {'cart_items': cart_items})

@csrf_exempt
def remove_from_cart(request):
    if request.method == "POST":
        key = request.POST.get('item_key')
        cart = request.session.get('cart', {})
        if key in cart:
            del cart[key]
            request.session['cart'] = cart
    return redirect('cart')

@csrf_exempt
def update_cart_quantity(request):
    if request.method == "POST":
        key = request.POST.get('item_key')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        if key in cart:
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
    return render(request, 'product_list', {'categories': categories, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})

















