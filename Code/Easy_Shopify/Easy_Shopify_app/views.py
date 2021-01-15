from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group, User, auth
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def home_view(request):
  
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else: 
        product_count_in_cart=0
        
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')	    
    return render(request,'Easy_Shopify_app/index.html',{'products':products, 'product_count_in_cart':product_count_in_cart})

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

def cart_view(request):
    
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
        
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)
            for p in products:
                total=total+p.price
                
    return render(request,'Easy_Shopify_app/cart.html',{'product_count_in_cart':product_count_in_cart,'products':products,'total':total})

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
    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    
    easy_shopify_app={
        'customercount':customercount,
        'productcount':productcount,
    }
    return render(request,'Easy_Shopify_app/admin_dashboard.html',context=easy_shopify_app)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')

@user_passes_test(is_customer)
def customer_home_view(request):
    
    return render(request,'Easy_Shopify_app/customer_home.html')

@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'Easy_Shopify_app/view_customer.html',{'customers':customers})

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

def add_to_cart_view(request,pk):
    products=models.Product.objects.all()

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'Easy_Shopify_app/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)
        product=models.Product.objects.get(id=pk)
        messages.info(request, product.name + ' Product successfully added to cart')
    return response

def remove_from_cart_view(request,pk):
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products=models.Product.objects.all().filter(id__in = product_id_in_cart)
        
        for p in products:
            total=total+p.price
    
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'Easy_Shopify_app/cart.html',{'product_count_in_cart':product_count_in_cart,'total':total,'products':products, 'product_id_in_cart':product_id_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response
    
@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')

@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'Easy_Shopify_app/admin_update_product.html',{'productForm':productForm})

def search_view(request):
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0  
    word="Searched Result :"
    if request.user.is_authenticated:
        return render(request,'Easy_Shopify_app/customer_home.html',{'products':products,'product_count_in_cart':product_count_in_cart,'word':word})
    return render(request,'Easy_Shopify_app/index.html',{'products':products,'product_count_in_cart':product_count_in_cart,'word':word})
