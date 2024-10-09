from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:name_id>/', views.view, name='product/<product_id>/'),
    path('process_order/', views.processOrder, name='process_order'),
    path('update_item/', views.updateItem, name='update_item'),
    path('contact-us/', views.contact, name='contact-us'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register_view, name='register'),
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name='store/reset_password.html'),
    name ='reset_password'),
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name='store/reset_password_sent.html'), 
    name ='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name='store/reset_password_confirm.html'),
    name ='password_reset_confirm'),
    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='store/reset_password_complete.html'),
    name ='password_reset_complete'),
    path('login/', views.login_view, name ='login'),
    path('driver-signup/', views.driver_signup_view, name='driver_signup'),
    path('driver-login/', views.driver_login, name='driver_login'),
    path('logout/', views.logout_view, name ='logout'),
    path('deliveries/', views.all_deliveries, name='all_deliveries'),
    path('my-deliveries/', views.user_delivery_status, name='user_delivery_status'),
    # path('driver-deliveries/', views.driver_deliveries, name='driver_deliveries'),
]
