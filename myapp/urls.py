from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'myapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.AuthenticateView.as_view(), name='authenticate'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('template/', views.templateview, name='template'),
    path("accounts/", include("django.contrib.auth.urls")),



    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    path('place_order', views.place_order, name='place_order'),

]
