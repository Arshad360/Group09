"""Easy_Shopify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from Easy_Shopify_app import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='Easy_Shopify_app/adminlogin.html')),
    path('customerclick', views.customerclick_view),
    path('customersignup', views.customer_signup_view),  
    path('customerlogin', LoginView.as_view(template_name='Easy_Shopify_app/customerlogin.html'),name='customerlogin'), 
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('customer-home', views.customer_home_view,name='customer-home'), 
]
