from django.contrib import admin
from .models import *

admin.site.site_header = "Pictura ::.."
admin.site.index_title = "Root Dashboard"
admin.site.site_title = "Pictura"


class AllProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'inStock', 'price', 'quantity', 'unit']
    list_editable = ['inStock', 'price', 'quantity', 'unit']


admin.site.register(AllProduct, AllProductAdmin)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(VerifyEmail)
admin.site.register(Category)


class OrderListAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'productName', 'price', 'quantity', 'total']


admin.site.register(OrderList, OrderListAdmin)
admin.site.register(OrderPending)

admin.site.register(Materials)
admin.site.register(Products)
