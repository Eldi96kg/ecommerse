from django.urls import path, include
from .views import *
from rest_framework import routers

app_name = 'ecomapp'

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact-us/', ContactView.as_view(), name='contact'),
    path('all-products/', AllProductsView.as_view(), name='allproducts'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='productdetail'),
    path('add-to-cart-<int:pro_id>/', AddToCartView.as_view(), name='addtocart'),
    path('my-cart/', MyCartView.as_view(), name='mycart'),
    path('manage-cart/<int:cp_id>/', ManageCartView.as_view(), name='managecart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('register/', CustomerRegistrationView.as_view(), name='customerregistration'),
    path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),
    path('login/', CustomerLoginView.as_view(), name='customerlogin'),
    path('api/',ProductList.as_view() ),
]




