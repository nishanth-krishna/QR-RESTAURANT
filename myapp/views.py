from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponse
from .models import Category, Food, Table, Cart, OrderItem, Images
from QR_Restaurant import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
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
        ctx = {
            'category':category,
            'food':food
        }
        return render(request, 'myapp/menu.html', ctx)
        
class CartView(LoginRequiredMixin,View):
    def get(self, request):
        mycart = Cart.objects.all()
        ctx = {
            'mycart':mycart,
        }
        return render(request, 'myapp/cart.html', ctx)






def templateview(request):
    return render(request, 'myapp/template.html')

def readQR(my_dict):
    d = cv2.QRCodeDetector()
    mystring = str(my_dict['mystr'])
    lol = "static/uploads/"+mystring.split('/')[-1]
    a,b,c = d.detectAndDecode(cv2.imread(lol))
    return int(a)
        