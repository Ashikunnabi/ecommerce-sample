from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .models import Profile

def has_access(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            request.role = str(Profile.objects.get(user=request.user).account_type)
            if request.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrap
    return decorator
