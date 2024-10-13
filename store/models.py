from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings  
import random
import string
from datetime import timedelta
from django.utils.text import slugify

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=23234232)
    first_name = models.CharField(max_length=23234232)
    last_name = models.CharField(max_length=23234232)
    department = models.CharField(max_length=4000)
    level = models.CharField(max_length=10)

    email = models.CharField(max_length=23234232)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)  # Adjust max_length for better limits
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # Description field added
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug field added
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Automatically generate the slug from the name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=23234232)
    def __str__(self):
        return self.customer.name
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def delivery_status(self):
        return self.delivery.status if hasattr(self, 'delivery') else 'No Delivery'
    

class DeliveryDriver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    current_deliveries = models.IntegerField(default=0)  # Track the number of active deliveries

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.current_deliveries} deliveries"


class Delivery(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    DELIVERY_METHOD_CHOICES = [
        ('STANDARD', 'Standard'),
        ('EXPRESS', 'Express'),
        ('SAME_DAY', 'Same Day'),
    ]

    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='delivery')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHOD_CHOICES, default='STANDARD')
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='PENDING')
    tracking_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    delivery_fee = models.FloatField(default=0.0)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    driver = models.ForeignKey('DeliveryDriver', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically calculate the estimated delivery date (10 days from order date) if not set
        if not self.estimated_delivery_date:
            self.estimated_delivery_date = self.order.date_order + timedelta(days=10)
        
        # Generate a tracking number if not already set
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        
        super(Delivery, self).save(*args, **kwargs)

    def generate_tracking_number(self):
        """
        Generate a unique tracking number consisting of random letters and numbers.
        """
        import random
        import string
        length = 10  # Define the length of the tracking number
        characters = string.ascii_uppercase + string.digits  # Use uppercase letters and digits
        tracking_number = ''.join(random.choice(characters) for _ in range(length))

        # Ensure the tracking number is unique
        while Delivery.objects.filter(tracking_number=tracking_number).exists():
            tracking_number = ''.join(random.choice(characters) for _ in range(length))

        return tracking_number

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # Measurement fields
    shirt_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    body_chest = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    back_shoulder = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sleeve = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    round_sleeve = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    round_mouth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    trouser_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    thigh_laps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    knee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    trouser_mouth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Special measurements
    half_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    full_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cap_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # def __str__(self):
    #     return self.product

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
class View(models.Model):
    product= models.OneToOneField(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0, blank=True, null=True)
    text = models.TextField()


    def __str__(self):
        return self.product.name

class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=40)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=40)

    def __str__(self):
        return self.customer.name
    
    @property
    def full_address(self):
        return f"{self.address}, {self.state}, {self.country}, {self.zipcode}"