from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group, User, auth
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test

def home_view(request):

    return render(request,'Easy_Shopify_app/index.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

def cart_view(request):
    return render(request,'Easy_Shopify_app/cart.html')
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')

def customerclick_view(request):
    
    return render(request, 'Easy_Shopify_app/customerlogin.html')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()     
    easy_shopify_app={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    
    return render(request,'Easy_Shopify_app/customersignup.html',context=easy_shopify_app)

@login_required(login_url='adminlogin') 
def admin_dashboard_view(request):
    
    return render(request,'Easy_Shopify_app/admin_dashboard.html')

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')

@user_passes_test(is_customer)
def customer_home_view(request):
    
    return render(request,'Easy_Shopify_app/customer_home.html')

def view_customer_view(request):
    return render(request, 'Easy_Shopify_app/view_customer.html')

@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'Easy_Shopify_app/admin_products.html',{'products':products})

@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'Easy_Shopify_app/admin_add_products.html',{'productForm':productForm})