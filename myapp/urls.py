from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'myapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.AuthenticateView.as_view(), name='authenticate'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('template/', views.templateview, name='template'),
    path("accounts/", include("django.contrib.auth.urls")),
]
