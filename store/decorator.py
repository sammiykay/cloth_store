from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import DeliveryDriver

def non_driver_required(view_func):
    """
    Decorator that restricts access to the view for delivery drivers.
    Only non-delivery drivers can access views decorated with this.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and has a delivery driver profile
        if request.user.is_authenticated:
            if hasattr(request.user, 'deliverydriver'):
                # If the user is a delivery driver, restrict access
                return redirect('all_deliveries')        
        # If not a delivery driver, allow access to the view
        return view_func(request, *args, **kwargs)

    return _wrapped_view
