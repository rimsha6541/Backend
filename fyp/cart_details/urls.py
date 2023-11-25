from django.urls import path
from .views import *

urlpatterns = [
    path('addtocart/', AddToCartView.as_view(), name="add to Cart"),
    path('cart/updated/', CartView.as_view(), name="Update_Cart"),
    path('cart/<int:id>', CartView.as_view(), name="Cart"),
    path('total/<int:id>', CartTotalView.as_view(), name="Cart total"),
    path('cartcount/<int:id>', CartCountView.as_view(), name="CartCount"),
    path('cart/delete/', DeleteCartView.as_view(), name="Cart-delete"),
    path('addtocartB2B/', AddToCartB2BView.as_view(), name="Cart-delete"),
    path('b2b/updated/', UpdateCartB2BView.as_view(), name="Cart-delete"),
    path('b2bcart/<int:id>', UpdateCartB2BView.as_view(), name="Cart-delete"),
]