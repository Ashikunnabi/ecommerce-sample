from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from ecommerce.models import Cart, Order, Product, Profile

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import (
    ProductsSerializer, 
    ProductListSerializer,
    ProfileSerializer,
    UserSerializer,
    OrderSerializer,
)
from rest_framework.generics import(
    ListAPIView,
)
from rest_framework.viewsets import(
    ModelViewSet,    
)
    

    
class LoginAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def post(self, request):        
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else: 
            context = {
             'message': 'Invalid Credentials.'
            }  
            return Response(data=context, status=200, template_name="ecommerce/authentication.html")
    
    
class LogoutAPIView(APIView):
    def get(self, request):        
        logout(request)
        return redirect('index')

 
class UserRegistrationAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
           
    def post(self, request):        
        data = request.data
        try:
            # creating new user
            password = data['password']
            user = User()
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.set_password(password)
            user.save()
            # creating user profile
            profile = Profile()
            profile.mobile_no = data['mobile_no']
            profile.account_type = data['account_type']
            profile.user = user
            profile.save()
            
            context = {
             'message': 'Successfully registered.'
            }
        except:
            context = {
             'message': 'Registration failed.'
            }
        
        return Response(data=context, status=200, template_name="ecommerce/authentication.html")

    
    
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
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = Profile.objects.get(user__id=request.user.id)
        p_serializer = ProfileSerializer(profile).data
        user = User.objects.get(id=request.user.id)
        u_serializer = UserSerializer(user).data
        return Response({
            'user'   : u_serializer,
            'profile': p_serializer
        })
    
    
class SellerWiseProductsAPIView(APIView):
    '''
    Sellers view for watching products
    customizing products
    '''
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        products = Product.objects.filter(seller__user__id=request.user.id)
        serializer = ProductsSerializer(products, many=True).data
        return Response(serializer)
    
 
class UserRegistrationAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
           
    def post(self, request):        
        data = request.data
        try:
            # creating new user
            password = data['password']
            user = User()
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.set_password(password)
            user.save()
            # creating user profile
            profile = Profile()
            profile.mobile_no = data['mobile_no']
            profile.account_type = data['account_type']
            profile.user = user
            profile.save()
            
            context = {
             'message': 'Successfully registered.'
            }
        except:
            context = {
             'message': 'Registration failed.'
            }
        
        return Response(data=context, status=200, template_name="ecommerce/authentication.html")

   
    
class BuyerOrderAPIView(APIView):
    '''
    Previous order view Buyer
    '''
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders     = Order.objects.filter(user=request.user)        
        serializer = OrderSerializer(orders, many=True).data
        return Response(serializer) 
        
    
class BuyerOrderDetailAPIView(APIView):
    '''
    Previous order view Buyer
    '''
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        orders     = Order.objects.filter(user=request.user, id=id)        
        serializer = OrderSerializer(orders, many=True).data
        return Response(serializer)  
    
    
class SellerOrderAPIView(APIView):
    '''
    Seller order view
    '''
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders     = Order.objects.filter(items__product__seller__user=request.user)
        serializer = OrderSerializer(orders, many=True).data
        return Response(serializer)
        
  

















    
        