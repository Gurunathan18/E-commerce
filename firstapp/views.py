import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from firstapp.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def home(request):
     products=product.objects.filter(trending=1)
     return render(request,"shop/index.html",{"p":products})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
      if request.method=="POST":
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Login  Succesfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid User Name or password")
    return render(request,"shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
    return redirect("/")


def register(request):
    form=CustomUserForm()
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success")
            return redirect('/login')
    return render(request,"shop/register.html",{'form':form})

def collections(request):
    c=catagory.objects.filter(status=0) 
    return render(request,"shop/collections.html",{"catagory":c})

def collectionsview(request,name):
    if(catagory.objects.filter(name=name,status=0)):
        products=product.objects.filter(catagory__name=name)
        return render(request,"shop/products/index.html",{"products":products,"catagory":name})
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect('collections')
def product_details(request,cname,pname):
    if(catagory.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            products=product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.warning(request,"No Such Product Found")
            return redirect('collections')
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect('collections')
    
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                   return JsonResponse({'status':'product Already in cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'product add to Cart success'},status=200)
                    else:
                        return JsonResponse({'status':'product stocknot available'},status=200)
        else:
          return JsonResponse({'status':'Log in to add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart}) 
    else:
        return redirect("/")   
def remove_cart(request,cid):
    cart=Cart.objects.get(id=cid)
    cart.delete()
    return redirect("/cart")