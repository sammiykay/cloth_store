from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import json
from .models import Product, Customer, Order, OrderItem, View
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import time
from django.contrib import messages
from .forms import *
from django.core.files import File
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .decorator import *
import datetime
# Create your views here.
from django.shortcuts import get_object_or_404, render

@ non_driver_required
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request,'store/store.html', context)


@ non_driver_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    return render(request, 'store/product_detail.html', {'product': product, 'cartItems': cartItems})


@ non_driver_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        messages.error(request, 'You need to login')
        return redirect('/login')
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'store/cart.html', context)

@ non_driver_required
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        messages.error(request, 'You need to login')
        return redirect('/login')
        
    
    context = {
        'cartItems': cartItems,
        'items': items,
        'order': order,
    }
    return render(request, 'store/checkout.html', context)

@ non_driver_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.delete()
        
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = cartItems = order.get_cart_items
    return JsonResponse(f'{cartItems}', safe=False)

@ non_driver_required
def view(request, name_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    product = Product.objects.get(id=name_id)
    views = View.objects.filter(product=product)
    context = {
        'views': views,
        "cartItems": cartItems
    }
    return render(request, 'store/views.html', context)

@ non_driver_required
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validation checks
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose a different one.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return redirect('register')

        # Create and log in the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        customer = Customer.objects.create(user=user, name=username)

        messages.success(request, "Registration successful " + username.upper() + "!")
        return redirect('login')  # Redirect to the home page or dashboard

    return render(request, 'store/register.html')


@ non_driver_required
def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    if request.method == 'POST':
        form = Contact(request.POST, files=request.FILES)
        if form.is_valid():
            print('message')
            user = form.save()
            obj = form.instance
            messages.success(request, 'Details Submitted')
            return redirect('/contact-us')
    else:
        form = Contact()
    return render(request, 'store/contact.html', {'form': form, 'cartItems': cartItems})



    
@ non_driver_required
def assign_driver_to_delivery(delivery):
    # Get the driver with the least number of active deliveries
    driver = DeliveryDriver.objects.order_by('current_deliveries').first()

    if driver:
        # Assign the driver to the delivery
        delivery.driver = driver
        delivery.save()

        # Increase the driver's workload
        driver.current_deliveries += 1
        driver.save()

    return driver
 

@ non_driver_required
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        print(order.shipping)
        shipping = Shipping.objects.create(
                customer = customer,
                order=order,
                address = data['shipping']['address'],
                zipcode = data['shipping']['zipcode'],
                country = data['shipping']['country'],
                state = data['shipping']['state'],
                )
        print(shipping.address)
        delivery = Delivery.objects.create(
                order=order,
                customer=customer,
                address=f"{shipping.address}, {shipping.state}, {shipping.country}, {shipping.zipcode}",
                delivery_method=data.get('delivery_method', 'STANDARD'),  # 'STANDARD' by @ non_driver_required
                delivery_fee=data.get('delivery_fee', 1500.00), 
                status='PENDING',  # Initial status
            )
        assign_driver_to_delivery(delivery)
    else:
        print('user is not logged in')
    print('Data:', request.body)
    return JsonResponse('Payment Complete!', safe=False)




def send_driver_id(driver):
    # Prepare the context for the email template
    context = {
        'driver': driver,
    }

    # Load HTML template and generate email content
    html_content = render_to_string('store/driver_email.html', context)  # This is the HTML template
    text_content = strip_tags(html_content)  # Strip HTML tags to create a plain text version

    # Prepare the email
    subject = 'Your account has been created'
    from_email = 'kayodeola47@gmail.com'
    to_email = [driver.email]  # Customer's email

    # Create the email with both HTML and plain text
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send(fail_silently=False)






def mark_delivery_as_completed(delivery):
    if delivery.status == 'DELIVERED' and delivery.driver:
        # Decrease the driver's current deliveries count
        delivery.driver.current_deliveries -= 1
        delivery.driver.save()

def send_delivery_update_email(delivery):
    # Prepare the context for the email template
    context = {
        'delivery': delivery,
    }

    # Load HTML template and generate email content
    html_content = render_to_string('store/delivery_status_update.html', context)  # This is the HTML template
    text_content = strip_tags(html_content)  # Strip HTML tags to create a plain text version

    # Prepare the email
    subject = 'Your Delivery Status Has Been Updated'
    from_email = 'kayodeola47@gmail.com'
    to_email = [delivery.customer.user.email]  # Customer's email

    # Create the email with both HTML and plain text
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")

    # Send the email
    try:
        email.send(fail_silently=False)
    except Exception as e:
        print(f"Error sending email: {e}")



@login_required
def all_deliveries(request):
    try:
        # Check if the user is a delivery driver by accessing the related DeliveryDriver model
        driver = request.user
        if DeliveryDriver.objects.filter(user=driver).exists():
            print('sam')
        else:
            return HttpResponse("You can't view this page. It only for drivers", status=403)

    except DeliveryDriver.DoesNotExist:
        return HttpResponse("You can't view this", status=403)
        messages.error(request, "You do not have permission to view this page.")
    driver = DeliveryDriver.objects.get(user=driver)

    # Filter deliveries for the logged-in delivery driver
    deliveries = Delivery.objects.filter(driver=driver)
    
    # List of forms matching the deliveries
    forms = [DeliveryStatusUpdateForm(instance=delivery) for delivery in deliveries]

    # Zip deliveries and forms
    deliveries_with_forms = zip(deliveries, forms)

    if request.method == 'POST':
        delivery_id = request.POST.get('delivery_id')
        delivery = Delivery.objects.get(id=delivery_id)
        form = DeliveryStatusUpdateForm(request.POST, instance=delivery)

        if form.is_valid():
            form.save()
            send_delivery_update_email(delivery)
            if delivery.status == 'DELIVERED':
                mark_delivery_as_completed(delivery)
            messages.success(request, f"Delivery status for Tracking Number {delivery.tracking_number} updated successfully.")
            return redirect('all_deliveries')  # Refresh the page

    context = {
        'deliveries_with_forms': deliveries_with_forms,  # Pass zipped data
    }
    return render(request, 'store/deliveries.html', context)

@login_required
@non_driver_required
def user_delivery_status(request):
    # Get the customer associated with the logged-in user
    customer = request.user.customer

    # Get all deliveries associated with the customer
    deliveries = Delivery.objects.filter(customer=customer)

    context = {
        'deliveries': deliveries,
    }
    
    return render(request, 'store/user_delivery_status.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')




def driver_signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Basic validation (you can expand this)
        if not username or not email or not phone_number or not password1 or not password2:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'store/driver_signup.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/driver_signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'store/driver_signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'store/driver_signup.html')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
        )

        # Create a DeliveryDriver profile linked to this user
        DeliveryDriver.objects.create(user=user, phone_number=phone_number)

        # Log the user in
        login(request, user)
        messages.success(request, f'Signup successful! Welcome, {username}!')
        return redirect('store')

    return render(request, 'store/driver_signup.html')


def driver_login(request):
    if request.method == 'POST':
        matric_number = request.POST.get('matric_number')
        password = request.POST.get('password')
        user = authenticate(request, matric_number=matric_number, password=password)

        if user is not None:
            if hasattr(user, 'deliverydriver'):
                login(request, user)
                messages.success(request, "Logged in successfully! ")
                return redirect('all_deliveries')  # Redirect to a driver-specific dashboard
            else:
                messages.error(request, "You are not registered as a delivery driver.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'store/driver_login.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validation checks
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('login')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, f"Welcome back, {username}!")
            return redirect('store')  # Redirect to the home page or dashboard
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')

    return render(request, 'store/login.html')