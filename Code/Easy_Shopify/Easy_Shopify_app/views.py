from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.

def home_view(request):

    return render(request,'Easy_Shopify_app/index.html')

def adminclick_view(request):
    
    return HttpResponseRedirect('adminlogin')

def customerclick_view(request):
    
    return render(request, 'Easy_Shopify_app/customerlogin.html')

def customersignupclick_view(request):                                            
                   
    return render(request, 'Easy_Shopify_app/customersignup.html')