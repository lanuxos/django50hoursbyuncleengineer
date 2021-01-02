# myapp's urls.py
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', Home, name='home-page'),
    path('about/', About, name='about-page'),
    path('contact/', Contact, name='contact-page'),
    path('portrait/', Portrait, name='portrait'),
    path('addProduct/', AddProduct, name='addProduct'),
    path('allProduct/', Product, name='allProduct'),
    path('register/', Register, name='register'),
    path('addToCart/<int:pid>', AddToCart, name='addToCart'),
    path('myCart/', MyCart, name='myCart'),
    path('myCart/edit/', MyCartEdit, name='myCartEdit'),
    path('checkOut/', CheckOut, name='checkOut'),
    path('orderList/', OrderListPage, name='orderList'),
    path('allOrderList/', AllOrderListPage, name='allOrderList'),
    path('uploadSlip/<str:orderId>', UploadSlip, name='uploadSlip'),
    path('updateStatus/<str:orderId>/<str:status>',
         UpdatePaid, name='updateStatus'),
    path('updateTracking/<str:orderId>/',
         UpdateTracking, name='updateTracking'),
    path('myOrder/<str:orderId>', MyOrder, name='myOrder'),
    path('testFunction/', TestFunction, name='testFunction'),
    path('confirm/<str:token>/', Confirm, name='confirmEmail'),
    path('category/<int:code>', ProductCategory, name='categoryPage'),
    path('graph/', Graph, name='graphPage'),
]
