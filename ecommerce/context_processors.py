from .models import Cart, Category, Profile

      
def common_context(request):
    # Counting cart items
    cart_items_count = Cart.objects.all().count
    
    # Checking user's account_type for user dashboard
    account_type = None
    try:
        account_type = str(Profile.objects.get(user=request.user).account_type)
    except:
        account_type = None  
        
    context = {        
      'account_type': account_type,
      'cart_items_count': cart_items_count,
      'categories': Category.objects.all(),
    }
    return context
                

        
        
        
        
        