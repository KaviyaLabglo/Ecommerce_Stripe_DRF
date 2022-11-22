from django.contrib import admin

# Register your models here.
from django.contrib import admin
from myapp.models import *

class S(admin.ModelAdmin):
    list_display = ('id','brand','image', 'title','price',  'availability', 'color')
admin.site.register(Product,S)

class add(admin.ModelAdmin):
    list_display = ('id','user', 'product_id', 'quantity','selling_price', 'is_active')
admin.site.register(Cart,add)

class ord(admin.ModelAdmin):
    list_display = ('id','order_user', 'order_status', )
admin.site.register(Order,ord)

class a(admin.ModelAdmin):
    list_display = ('id','user1', 'product1','price', 'is_active1' )
admin.site.register(Wishlist,a)


admin.site.register(Brand)