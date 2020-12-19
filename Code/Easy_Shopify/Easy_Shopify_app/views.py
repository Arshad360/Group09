from django.shortcuts import render,redirect
from . import forms,models
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group, User, auth
from django.conf import settings


def home_view(request):

    return render(request,'Easy_Shopify_app/index.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

def afterlogin_view(request):
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
