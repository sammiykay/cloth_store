from django.contrib import admin
from .models import *


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(View)
admin.site.register(ContactUs)
admin.site.register(Shipping)
admin.site.register(Delivery)
admin.site.register(DeliveryDriver)
# Register your models here.