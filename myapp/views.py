from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from .models import Category, Food, Table, Cart, OrderItem, Images
from QR_Restaurant import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import cv2

# Create your views here.

class AuthenticateView(View):
    def get(self, request):
        return render(request, 'myapp/authenticate.html')
    def post(self, request):
        table = Table()
        img = Images()
        table.table_owner_phone_number = request.POST.get('phone')
        
        img.image = request.FILES['qr']
        img.save()
        #table.table_login = True    
        #table.table_number=10
        #table.save()
        mystr = img.image.url
        ctx = {
            'img':img,
            'mystr':mystr
        }
        ctx['result']=readQR(ctx)
        table.table_number=ctx['result']
        user = User.objects.create_user(table.table_owner_phone_number, 'aaromale@login.com', 'aaromale')
        user.save()
        login(request, user)
        table.table_user=request.user
        table.save()
        
        #user_auth = authenticate(username=table.table_owner_phone_number, password='aaromale')
        return redirect(reverse_lazy('myapp:menu'))
        #return render(request, 'myapp/lol.html',ctx)
    
class MenuView(LoginRequiredMixin,View):
    def get(self, request):
        category = Category.objects.all()
        food = Food.objects.all()
        table = Table.objects.get(table_user=request.user)
        ctx = {
            'category':category,
            'food':food,
            'table':table,
        }
        return render(request, 'myapp/menu.html', ctx)
        
class CartView(LoginRequiredMixin,View):
    def get(self, request):
        mycart = Cart.objects.filter(cart_user=request.user)
        total_price=0
        for item in mycart:
            total_price += item.cart_food.food_price*item.cart_food_qty
        ctx = {
            'mycart':mycart,
            'total_price':total_price,
        }
        return render(request, 'myapp/cart.html', ctx)

class OrdersView(View):
    def get(self, request):
        orders = OrderItem.objects.filter(orderitem_user=request.user)
        total_price = 0
        for item in orders:
            total_price += (item.order_price)*(item.order_quantity)
        ctx = {
            'orders':orders,
            'total_price':total_price,
        }
        return render(request, 'myapp/orders.html', ctx)








def templateview(request):
    return render(request, 'myapp/template.html')

def readQR(my_dict):
    d = cv2.QRCodeDetector()
    mystring = str(my_dict['mystr'])
    lol = "static/uploads/"+mystring.split('/')[-1]
    a,b,c = d.detectAndDecode(cv2.imread(lol))
    return int(a)

def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            food_id = int(request.POST.get('food_id'))
            food_qty = int(request.POST.get('food_qty'))
            table_id = int(request.POST.get('table_id'))
            table = Table.objects.get(table_number = table_id)

            food_check = Food.objects.get(pk=food_id)
            if food_check:
                if Cart.objects.filter(cart_user=request.user, cart_food=food_check):
                    adding_qty = Cart.objects.get(cart_user=request.user, cart_food=food_check)
                    adding_qty.cart_food_qty += food_qty
                    adding_qty.save()
                    return JsonResponse({'status':'it is already in cart broooo so I add the quantity'})
                else:
                    if food_check.food_quantity_available>food_qty:
                        Cart.objects.create(cart_user=request.user, cart_food=food_check, cart_food_qty=food_qty, cart_table=table)
                        return JsonResponse({'status':'Added to cart'})
                    else:    
                        return JsonResponse({'status':'Only '+str(food_check.food_quantity_available)+' units available'})
            
            else:
                return JsonResponse({'status':'no such product found'})    


        else:
            return JsonResponse({'status':'Login to continue'})
    return redirect('/')

def remove_from_cart(request):
    if request.method == 'POST':
        food_id = int(request.POST.get('food_id'))
        product_check = Food.objects.get(pk=food_id)
        if product_check:
            if Cart.objects.filter(cart_user=request.user, cart_food=product_check):
                Cart.objects.filter(cart_user=request.user, cart_food=product_check).delete()
                return JsonResponse({'status':'Product removed from the cart'})
            else:
                return JsonResponse({'status':'Product not in the cart'})
        else:    
            return JsonResponse({'status':'No such product'})
    
    return redirect('/')

def place_order(request):
    if request.method == 'POST':
        mycart = Cart.objects.filter(cart_user=request.user)
        table = Table.objects.get(table_user = request.user)
        if mycart:
            for item in mycart:
                OrderItem.objects.create(orderitem_user=request.user, order_table=table, ordered_food=item.cart_food, order_price=item.cart_food.food_price, order_quantity=item.cart_food_qty)
            
            Cart.objects.filter(cart_user=request.user).delete()
            return JsonResponse({'status':'Order placed'})
    
    return redirect('/')
        