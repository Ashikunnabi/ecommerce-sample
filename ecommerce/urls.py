from django.urls import include, path
from .views import (
    add_to_cart,
    authentication,
    buyer,
    buyer_order_detail_view,
    category_wise_view,
    checkout,
    index,
    order,
    product,
    seller,
    seller_add_product,
    seller_edit_product,
    seller_delete_product,
    seller_order_detail_view,
)


urlpatterns = [
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('authentication/',authentication, name='authentication'),
    path('buyer/', buyer, name='buyer'),
    path('buyer-order/<int:id>', buyer_order_detail_view, name='buyer_order'),
    path('category-wise/<int:id>', category_wise_view, name='category_wise_view'),
    path('checkout/', checkout, name='checkout'),
    path('',index, name='index'),
    path('order/', order, name='order'),
    path('product/<int:id>', product, name='product'),
    path('seller/', seller, name='seller'),
    path('add-product/', seller_add_product, name='add_product'),
    path('edit-product/<int:id>', seller_edit_product, name='edit_product'),
    path('delete-product/<int:id>', seller_delete_product, name='delete_product'),
    path('seller-order/<int:id>', seller_order_detail_view, name='seller_order'),
    
    # api routers
    path('api/', include('ecommerce.api.urls')),
]
