from django.urls import path
from . import views

urlpatterns = [
    path('customer/signup/verify-otp/', views.verify_otp, name='verify_otp'),
    path('', views.mainpage, name='mainpage'),
    path('add-provider', views.add_provider, name='add_provider'),
    path('admin-login/', views.admin_login, name='admin_login'),          
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('customer/products/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/request/', views.request_product, name='request_product'),
    path('customer/', views.customer_entry, name='customer_entry'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/signup/', views.customer_signup, name='customer_signup'),
    path('provider/login/', views.provider_login, name='provider_login'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/logout/', views.provider_logout, name='provider_logout'),
    path('customer/orders/', views.customer_orders, name='customer_orders'),
    path('provider/mark-delivered/', views.mark_delivered, name='mark_delivered'),
    path('provider/deliveries/', views.view_deliveries, name='view_deliveries'),
    path('provider/decline/', views.decline_request, name='decline_request'),
    path('update_cell/', views.update_cell, name='update_cell'),
]
