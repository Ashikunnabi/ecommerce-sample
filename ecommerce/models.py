from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ACCOUNT_TYPE = (
        ('b', 'Buyer'),
        ('s', 'Seller'),
    )
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no    = models.CharField(max_length=15)
    account_type = models.CharField( max_length=1, choices=ACCOUNT_TYPE, default='b')
    
    def __str__(self):
        return self.user.username
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name        = models.CharField(max_length=50)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price       = models.PositiveIntegerField(default=0)
    quantity    = models.PositiveIntegerField(default=0)
    image       = models.FileField()
    seller      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
        
    def get_category_name(self):
        return self.category.name
        
    def get_seller_name(self):
        return self.seller.user.username
    

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.product.name
    
    def total_price(self):
        return (self.product.price * self.quantity)
        
    
class Order(models.Model):
    pass