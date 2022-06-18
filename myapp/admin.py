import imp
from django.contrib import admin
from .models import Category, Food, Table, Cart, OrderItem, Images

# Register your models here.
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Table)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Images)
