from os import name
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField
from django.utils.text import slugify

# Create your models here.

STATUS = (
    (0, "DRAFT"),
    (1, "PUBLISH")
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False, unique=True)
    datetime = models.DateTimeField(auto_now_add=True, editable= False)
    
    def save(self, *a, **k):
        self.slug = slugify(self.name)
        return super().save(*a, **k)

    class Meta:
        verbose_name_plural = 'categories'   

    def __str__(self):
        return self.name     

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False, unique=True)
    file = models.ImageField(upload_to = "images/") 
    price = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.BooleanField(choices=STATUS, default= True)
    
    def __str__(self):
        return self.name

    def save(self, *a, **k):
        self.slug = slugify(self.name)
        return super().save(*a, **k)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    paid = models.BooleanField(default= False)
    datetime = models.DateTimeField(auto_now_add=True, editable= False)

    def __str__(self):
        return f"{self.user} {self.paid}"   

    @property
    def get_cart_total(self):
        # return sum([c.get_product_price for c in self.cartdetails.all()])
        cartsdetails = self.cartdetails.all()  

        total = 0
        for c in cartsdetails:
            total += c.get_product_price

        return total 

class Cartdetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartdetails")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartdetails")
    quantity = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.cart.id} {self.product.name} [{self.quantity}]"

    @property
    def get_product_price(self):
        return self.product.price * self.quantity   

class Payment(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="payments")
    amount = models.FloatField(editable= False)
    total = models.FloatField(editable= False)
    reference = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True, editable=False)

class Deliverypoint(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=18)
    email = models.EmailField()
    address = models.CharField(max_length= 200)
    cart = models.OneToOneField(Cart, unique=True, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)
    delivered = models.BooleanField(default=False)