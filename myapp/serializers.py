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


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ["title","color", "price", "id"]
        


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["product", "quantity", "is_active", "id"]
        
        

class  WishlistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wishlist
        fields =["product"]
        
    
class  OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
    
    
        
        
        
        
       
        
        
