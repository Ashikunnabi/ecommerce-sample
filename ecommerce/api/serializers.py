from django.contrib.auth.models import User 
from ecommerce.models import(
    Cart,
    Product,
    Profile,
    Order,
)
from rest_framework.serializers import (
    StringRelatedField,
    ModelSerializer,
    CharField,
)  
     

class ProductsSerializer(ModelSerializer):
    category = CharField(source='get_category_name')
    seller   = CharField(source='get_seller_name')
    class Meta:
        model  = Product
        fields = '__all__'


class ProductListSerializer(ModelSerializer):
    category = CharField(source='get_category_name')
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'price', 'image']        
     

class ProfileSerializer(ModelSerializer):
    class Meta:
        model  = Profile
        fields = '__all__'       
     

class UserSerializer(ModelSerializer):
    class Meta:
        model  = User
        fields = '__all__'


        
class CartSerializer(ModelSerializer):
    product = ProductsSerializer()
    name = CharField(source='__str__')

    class Meta:
        model  = Cart
        fields = '__all__'  
        
        
class OrderSerializer(ModelSerializer):
    items = CartSerializer(many=True)

    class Meta:
        model  = Order
        fields = '__all__'  
        
        
        
        