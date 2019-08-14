from django.urls import include, path
from rest_framework import routers
from .viewsets import (
    LoginAPIView,
    LogoutAPIView,
    ProductsAPIView,
    ProductListAPIView, 
    ProfileAPIView, 
    SellerWiseProductsAPIView,
    BuyerOrderAPIView,
    BuyerOrderDetailAPIView,
    SellerOrderAPIView,
    UserRegistrationAPIView,
)  

router = routers.DefaultRouter()
router.register('product', ProductsAPIView)

urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('user-profile', ProfileAPIView.as_view()),
    path('seller', SellerWiseProductsAPIView.as_view()),
    path('registration', UserRegistrationAPIView.as_view(), name="registration"),
    path('login', LoginAPIView.as_view(), name="login"),
    path('logout', LogoutAPIView.as_view(), name="logout"),
    path('buyer-orders', BuyerOrderAPIView.as_view(), name="orders"),
    path('buyer-orders/<int:id>', BuyerOrderDetailAPIView.as_view(), name="orders_details"),
    path('seller-orders', SellerOrderAPIView.as_view(), name="orders"),
    path('', include(router.urls)),
]