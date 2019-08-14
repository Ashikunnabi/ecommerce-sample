from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import requests

from .api.end_point_base import end_point_base
from .decorators import has_access
from .models import Cart, Category, Order, Product, Profile 
from .forms import ProductForm


def authentication(request, *args, **kwargs):
    '''
    User registration and authentication both are done by api
    '''
    return render(request, 'ecommerce/authentication.html')

    
def category_wise_view(request, id):
    '''
    This view will show products filtering by category.
    Normal Django view.
    '''
    data = Product.objects.filter(category__id=id)
    context = {
        'data'    : data,
        'media'   : True, # Add {% get_media_prefix %} for image for relative path
        'category': Category.objects.get(id=id)   # Getting category name for toolbar
    }
    return render(request, 'ecommerce/index.html', context)
    
    
def index(request):
    '''
    This is showing the home page.
    List of products are shown using API call.
    'requests' module helps to hit the API end-point.
    '''
    # API call
    response  = requests.get('{}/?format=json'.format(end_point_base))
    # Converting response as JSON format
    json_data = response.json()
    
    context = {
        'data'        : json_data,
    }
    return render(request, 'ecommerce/index.html', context)
    
    
def product(request, id):
    '''
    This view is showing individual product details.
    api_endpoint helps to pass the api end-point to template
    so that ajax request can held to show details of the product.
    '''
    api_endpoint = '{}/product/{}?format=json'.format(end_point_base, id)
    context = {
        'url': api_endpoint,
    }
    return render(request, 'ecommerce/product.html', context)
    
    
@login_required(login_url='authentication')   
@has_access(['b'])
def buyer(request):
    '''
    Buyer's dashboard 
    Authentication needed to see dashboard.
    '''
    
    context = {
        'user_profile_url': '{}/user-profile?format=json'.format(end_point_base),
        'orders_url': '{}/buyer-orders?format=json'.format(end_point_base),
    }
    return render(request, 'ecommerce/buyer.html', context)
    
    
@login_required(login_url='authentication')   
@has_access(['b'])
def buyer_order_detail_view(request, id):
    '''
    Buyer's order history detail view 
    '''    
    context = {
        'orders_url': '{}/buyer-orders/{}?format=json'.format(end_point_base, id),
    }
    return render(request, 'ecommerce/checkout_complete.html', context)

    
@login_required(login_url='authentication')   
@has_access(['s'])   
def seller(request, id=None):
    '''
    Seller's dashboard 
    Authentication needed to see dashboard.
    '''
    # Users personal information by api end-point
    user_profile = '{}/user-profile?format=json'.format(end_point_base)
    if request.method == 'GET':
        products = '{}/seller?format=json'.format(end_point_base)
    else:
        products = '{}/seller/{}?format=json'.format(end_point_base, id)
    context = {
        'products_url'    : products,
        'user_profile_url': user_profile,
    }
    return render(request, 'ecommerce/seller.html', context)
    
    
@login_required(login_url='authentication')   
@has_access(['s'])      
def seller_add_product(request):
    if request.method == "POST":
        post_form = ProductForm(request.POST, request.FILES)
        if post_form.is_valid():
            obj          = post_form.save(commit=False)
            obj.seller   = Profile.objects.get(user=request.user)
            obj.category = Category.objects.get(id=request.POST['category'])
            obj.save()
        else:
            print(post_form.errors)
    return redirect(seller)
    
    
@login_required(login_url='authentication')   
@has_access(['s'])     
def seller_edit_product(request, id=None):
    if request.method == "GET":
        product = Product.objects.get(id=id)
        context = {
            'product': product
        }
        return render(request, 'ecommerce/product_edit.html',context)
        
    if request.method == "POST":
        product   = Product.objects.get(id=id)
        post_form = ProductForm(request.POST, request.FILES, instance=product)
        if post_form.is_valid():
            obj          = post_form.save(commit=False)
            obj.category = Category.objects.get(id=request.POST['category'])
            obj.save()
        else:
            print(post_form.errors)    
    return redirect(seller)
 
 
@login_required(login_url='authentication')   
@has_access(['s'])  
def seller_delete_product(request, id=None):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(seller)
    
         
def checkout(request):
    total_price = 0
    cart_items = Cart.objects.filter(ordered=False)
    
    # Counting total price 
    for item in cart_items:
        total_price += int(item.total_price())
        
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'ecommerce/checkout.html', context)    
    
    
def add_to_cart(request):
    '''
    Adding products/items into cart 
    '''
    if request.method == "POST":
        id       = request.POST['product_id']
        quantity = request.POST['quantity']
        increase = request.POST['increase_quantity']
        decrease = request.POST['decrease_quantity']
        page_url = request.POST['path']
        
        item     = Product.objects.get(id=id)
        
        # checking the item is already in cart
        try:
            item_in_cart = Cart.objects.get(product=item, ordered=False)
        except:
            item_in_cart = False
        if item_in_cart:
            if increase == "True":
                increase_quantity(item, quantity) 
            if decrease == "True":
                decrease_quantity(item) 
        else:
            Cart.objects.create(product=item, quantity=quantity)
    
    return redirect(page_url)   
    
    
def increase_quantity(item, quantity):        
    available_item = Cart.objects.get(product=item, ordered=False)
    if quantity is not '':
        available_item.quantity += int(quantity)
    else:
        available_item.quantity += 1
    available_item.save()   
    
    
def decrease_quantity(item):        
    available_item = Cart.objects.get(product=item, ordered=False)
    if available_item.quantity == 1:
        available_item.delete()
    else:
       available_item.quantity -= 1
       available_item.save()
    

@login_required(login_url='authentication')   
@has_access(['b'])    
def order(request):
    if request.method == "POST": 
        total_price = 0     
        cart_items = Cart.objects.filter(ordered=False)
        # Counting total price 
        for item in cart_items:
            total_price += int(item.total_price())
            
        order = Order.objects.create(
            user = request.user,
            total = total_price
        )
        order.items.set(cart_items)
        
        # Making the car item ordered = True 
        for cart_item in Cart.objects.filter(ordered=False):
            cart_item.ordered=True
            cart_item.save()
        
        context = {
            'message': "Order Placed Successfully.",
            'user_profile_url': '{}/user-profile?format=json'.format(end_point_base),
        }
        return render(request, 'ecommerce/buyer.html', context)
    else:
        return redirect(checkout)
    
    
    
    
