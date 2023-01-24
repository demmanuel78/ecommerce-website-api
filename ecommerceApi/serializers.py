from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password",]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= "__all__"
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= "__all__"
        
           
class CartSerializer(serializers.ModelSerializer):   
    cart_total = serializers.ReadOnlyField(source="get_cart_total")
    class Meta:
        model = Cart
        fields= "__all__"    
        
        
class CartdetailSerializer(serializers.ModelSerializer):
    product_price = serializers.ReadOnlyField(source="get_product_price")
    class Meta:
        model = Cartdetail
        fields= "__all__"
        
class PaymentSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Payment
        fields= "__all__"
        
class DeliverypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverypoint
        fields= "__all__"