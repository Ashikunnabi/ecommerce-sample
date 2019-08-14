from django.contrib import admin
from .models import Category, Cart, Order, Profile, Product


admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Product)
