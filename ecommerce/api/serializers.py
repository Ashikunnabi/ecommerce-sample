from django.contrib.auth.models import User 
from ecommerce.models import(
    Product,
    Profile,
)
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
)  
     

class AuthenticationSerializer(ModelSerializer):
    class Meta:
        model  = User
        fields = '__all__'
        

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