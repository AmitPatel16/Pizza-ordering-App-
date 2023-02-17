# from collections import UserDict
# from site import USER_SITE

from django.shortcuts import render,redirect
# from locust import User
from django.contrib.auth import login , authenticate
from home.models import *
from django.contrib import messages
from instamojo_wrapper import Instamojo
from django.conf import settings
api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN , endpoint="https://test.instamojo.com/api/1.1/")

# Create your views here.

def home(request):
   pizzas = Pizza.objects.all()
   context = {'pizzas' : pizzas}
   return render(request , 'home.html', context)


def login_page(request):
   if request.method == 'POST':
      try:
         username = request.POST.get('username')
         password = request.POST.get('password')

         user_obj = User.filter(username = username)
         if not user_obj.exists():
            messages.warning(request, 'User not found.')
            return redirect('/login/')

         user_obj = authenticate(username = username , password = password)
         if user_obj:
            login(request, user_obj)
            return redirect('/')

         messages.error(request, 'Wroung password. ')

         return redirect('/login/')

      except Exception as e:
         messages.success(request, 'Something went wrong.')

         return redirect('/register/')

   return render(request, 'login.html')


def register_page(request):
   if request.method == 'POST':
      try:
         username = request.POST.get('username')
         password = request.POST.get('password')

         user_obj = User.objects.filter(username = username)
         if user_obj.exists():
            messages.error(request, 'Username is taken')
            return redirect('/register/')

         user_obj = User.objects.create(username = username)
         user_obj.set_password(password)
         user_obj.save()

         messages.success(request, 'Account created.')

         return redirect('/login/')

      except Exception as e:
         messages.success(request, 'Something went wrong.')

         return redirect('/register/')         
         
   return render(request, 'register.html')



def add_cart(request , pizza_uid):
   user = request.user
   pizza_obj = Pizza.objects.get(uid = pizza_uid)
   cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
   cart_items = CartItems.objects.create(
       cart = cart,
       pizza = pizza_obj
   )

   return redirect('/')

def cart(request):
   cart = Cart.objects.get(is_paid = False , user = request.user)
   # response = api.payment_request_create(
   #    # amount= carts.get_cart_total(),
   #    purpose= "Order",
   #    buyer_name = request.user.username,
   #    email= "amit.patel00298@gamil.com",
   #    redirect_url= "http://127.0.0.1:8000/success/",
   # )
   context = {'carts' : cart }
   # , 'payment_url' : response['payment_request']['longurl']}
   # print(response)  
   return render(request , 'cart.html' , context)
   


def remove_cart_items(request , cart_item_uid):
   try:
      CartItems.objects.get(uid = cart_item_uid).delete()

      return redirect('/cart/')
   except Exception as e:
      print(e)


def orders(request):
   order = Cart.objects.filter(is_paid = True , user = request.user)
   context = {'order' : order}
   return render(request , 'order.html' ,context)




    
