from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def get_file_path(request, filename):
    original_filename = filename
    now = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (now, original_filename)
    return os.path.join('uploads/', filename)

class Images(models.Model):
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Table(models.Model):
    table_user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_number = models.IntegerField(null=False, blank=False)
    table_login = models.BooleanField(default=False)
    table_owner_phone_number = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return '_____ {} _____'.format(self.table_number)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100, null=False, blank=False)
    food_image_1 = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    food_desciption = models.TextField(null=False, blank=False)
    food_price = models.FloatField(null=False, blank=False)
    food_quantity_available = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.food_name

class Cart(models.Model):
    cart_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_table = models.ForeignKey(Table, on_delete=models.CASCADE)
    cart_food = models.ForeignKey(Food, on_delete=models.CASCADE)
    cart_food_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class Order(models.Model):
#     cart_table = models.ForeignKey(Table, on_delete=models.CASCADE)
#     total_amount = models.FloatField(null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return '{} - {}'.format(self.id, self.tracking_number)

class OrderItem(models.Model):
    orderitem_user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_table = models.ForeignKey(Table, on_delete=models.CASCADE)
    ordered_food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order_price = models.FloatField(null=False)
    order_quantity = models.IntegerField(null=False)
    order_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} _____ {} _____ {} _____ {}'.format(self.id, self.order_table, self.ordered_food, self.order_created_at)