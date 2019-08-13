from django.urls import include, path
from .views import (
    authentication,
    buyer,
    category_wise_view,
    checkout,
    index,
    product,
    seller,
    seller_add_product,
    seller_edit_product,
    seller_delete_product,
)


urlpatterns = [
    path('authentication/',authentication, name='authentication'),
    path('buyer/', buyer, name='buyer'),
    path('category-wise/<int:id>', category_wise_view, name='category_wise_view'),
    path('checkout/', checkout, name='checkout'),
    path('',index, name='index'),
    path('product/<int:id>', product, name='product'),
    path('seller/', seller, name='seller'),
    path('add-product/', seller_add_product, name='add_product'),
    path('edit-product/<int:id>', seller_edit_product, name='edit_product'),
    path('delete-product/<int:id>', seller_delete_product, name='delete_product'),
    
    # api routers
    path('api/', include('ecommerce.api.urls')),
]
