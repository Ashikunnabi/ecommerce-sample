from django.urls import include, path
from rest_framework import routers
from .viewsets import (
    AuthenticationAPIView,
    ProductsAPIView,
    ProductListAPIView, 
    ProfileAPIView, 
    SellerWiseProductsAPIView,
    SellerWiseProductsDetailAPIView,
)  

router = routers.DefaultRouter()
router.register('product', ProductsAPIView)
router.register('auth', AuthenticationAPIView)

urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('user-profile', ProfileAPIView.as_view()),
    path('seller', SellerWiseProductsAPIView.as_view()),
    path('seller/<int:id>', SellerWiseProductsDetailAPIView.as_view()),
    path('', include(router.urls)),
]