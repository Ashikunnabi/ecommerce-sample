from .serializers import (
    AuthenticationSerializer, 
    ProductsSerializer, 
    ProductListSerializer,
    ProfileSerializer,
    UserSerializer,
)
from django.shortcuts import get_object_or_404
from ecommerce.models import Product, Profile
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.generics import(
    ListAPIView,
)
from rest_framework.viewsets import(
    ModelViewSet,    
)
from rest_framework.views import APIView
from rest_framework.response import Response    

    
class AuthenticationAPIView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = AuthenticationSerializer
    lookup_field = 'id'  
    
    
class ProductsAPIView(ModelViewSet):
    queryset         = Product.objects.all()
    serializer_class = ProductsSerializer
    lookup_field     = 'id'
    

class ProductListAPIView(ListAPIView):
    queryset         = Product.objects.all()
    serializer_class = ProductListSerializer
    
    
class ProfileAPIView(APIView):
    '''
    User profile 
    '''
    
    def get(self, request):
        profile = Profile.objects.get(user__id=request.user.id)
        p_serializer = ProfileSerializer(profile).data
        user = User.objects.get(id=request.user.id)
        u_serializer = UserSerializer(user).data
        return Response({
            'user'   : u_serializer,
            'profile': p_serializer
        })
    
    def post(self, request):
        data = request.data
        
        p_data = { 
           'mobile_no': data['mobile_no'], 
        }
        
        u_data = { 
           'first_name': data['first_name'], 
           'last_name': data['last_name'], 
           'email': data['email'], 
           'password': data['password'],
        }
        print(data)
        try: 
            profile = Profile.objects.get(user__id=request.user.id)
            profile.mobile_no = data['mobile_no']
            profile.save()
            user = User.objects.get(id=request.user.id)
            user.first_name = data['first_name']
            user.last_name  = data['last_name']
            user.email      = data['email']
            user.set_password(data['password'])
            user.save()
            return Response(status=200)
        except:
            return Response(status=400)
    
    
class SellerWiseProductsAPIView(APIView):
    '''
    Sellers view for watching products
    customizing products
    '''
    
    def get(self, request):
        products = Product.objects.filter(seller__user__id=request.user.id)
        serializer = ProductsSerializer(products, many=True).data
        return Response(serializer)
    
    
class SellerWiseProductsDetailAPIView(APIView):
    '''
    Sellers view for watching products
    customizing products
    '''
    
    def get_object(self, id):
        try:
            return Product.objects.filter(id=id)
        except Product.DoesNotExit as e:
            return Response({'error': 'Product Does Not Exist'}, status=400)
    
    def get(self, request, id):
        product = self.get_object(id)
        serializer = ProductsSerializer(product, many=True).data
        return Response(serializer)
    
    def put(self, request, id):
        data = request.data
        product = self.get_object(id)
        serializer = ProductsSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)        
        return Response(serializer.errors, status=400)
    
    def delete(self, request, id):
        product = self.get_object(id)
        serializer = ProductsSerializer(product)
        serializer.delete()     
        return HttpResponse(serializer.errors, status=400)
        
        
        
        
        