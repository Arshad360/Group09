from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.

def home_view(request):

    return render(request,'Easy_Shopify_app/index.html')