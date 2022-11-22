from rest_framework import serializers

from myapp.models import (Product, 
    Brand,
    Cart,
    Wishlist,
    Order
    )


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title","color", "price", "id", "brand"]
        


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        
        

class  WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
        
    
class  OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
    
    
        
        
        
        
       
        
        
