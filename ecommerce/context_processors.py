from .models import Category

      
def common_context(request):    
    context = {        
      'categories': Category.objects.all(),
    }
    return context
                

        
        
        
        
        