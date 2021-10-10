from django.urls import path
from OrderApp.views import Add_to_Shoping_cart, cart_details, cart_delete, OrderCart

urlpatterns = [
    path('addingcart/<int:id>/', Add_to_Shoping_cart, name='Add_to_Shoping_cart'),
    path('cartdetails/<int:id>/', Add_to_Shoping_cart, name='Add_to_Shoping_cart'),
    path('cartdetails/', cart_details, name='cart_details'),
    path('deletecart/<int:id>/', cart_delete, name='cart_delete'),
    path('ordercart/', OrderCart, name='OrderCart'),


]
