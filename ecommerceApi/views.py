from django.core.checks import messages
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response
import requests
import math



class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    def retrieve(self, request, pk=None):
        queryset1 = get_object_or_404(Category, slug=pk)
        category = CategorySerializer(queryset1)
        return Response(category.data)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Category, slug=pk)
        queryset.delete()
        return Response({"message": "Category Deleted Successfully"})

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    def retrieve(self, request, pk=None):
        queryset1 = get_object_or_404(Product, slug=pk)
        product = ProductSerializer(queryset1)
        return Response(product.data)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Product, slug=pk)
        queryset.delete()
        return Response({"message": "Product Deleted Successfully"})
    
class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    #if user is no the same as the person the person that logged in
    def create(self, request):
        if not int(request.user.id) == int(request.POST.get("user")):
            return Response("{'message': 'you can't create cart for another username'}")
        cart = Cart.objects.filter(user=request.user, paid=False)

        if(len(cart) > 0):
            scart = CartSerializer(cart, many=True)
            return Response(scart.data)

        serializer = CartSerializer(data = request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    
    
class CartdetailView(viewsets.ModelViewSet):
    serializer_class = CartdetailSerializer
    queryset = Cartdetail.objects.all()
     
    def create(self, request):
        cart = Cartdetail.objects.filter(cart=request.POST.get("cart"), product=request.POST.get("product"))

        if(len(cart) > 0):
            scart = CartdetailSerializer(cart, many=True)
            return self.update(request=request, id=cart[0].id)

        serializer = CartdetailSerializer(data = request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
   
    def update(self, request, id):
        cartdetail = get_object_or_404(Cartdetail, id=id)
        # if the quantity is less than 1 then call the delete method
        if (int(request.POST.get("quantity") <1)):
            return self.delete(request=request, id= cartdetail.id) 

        serializer = CartdetailSerializer(data = request.POST, instance=cartdetail)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    def delete(self, request,id):
        cartdetail = get_object_or_404(Cartdetail, id=id)  
        cartdetail.delete()
        return Response({"message": "product has beem deleted"})

class PaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
 
    def create(self, request):
        #pipenv install requests
        #secret_key,ref,
        secret_key = "sk_test_2b8d99beebb74c885e5f5a385dbbf1bf5918d90f"
        reference = request.POST.get("reference")
        #endpoint for verification
        url = "https://api.paystack.co/transaction/verify/"+reference

        #headers that we will be sending
        headers = {
                "Authorization": "Bearer" + secret_key,
                "Cache-Control": "no-cache",
            }
        #make our api request to paystack
        response = requests.get(url, headers=headers)
        # response should be in JSON format
        response = response.json()

        #to check status
        if response["status"] == True:
            #insert into payment
            #check if a payment with that reference number doesn't exist

            #to check the total amount needed to be paid  for a cart
            cartid = request.POST.get("cart")
            cart = get_object_or_404(Cart, id=cartid)
            amount = float(cart.get_cart_total)
            paystacktotal = float(response["data"]["amount"]/100)

            #to see if the payment with the reference number has already been recorded
            checkreference = Payment.objects.filter(reference=reference).exists()           
            #to pass the values from our form to the PaymentSerializer
            serializer = PaymentSerializer(data=request.POST)
            # so if the reference number doesn't exists and the form values is valid
            if not checkreference and serializer.is_valid():
                #we can't add values coming from the form in an API
                serializer.save(amount=amount, total=paystacktotal)
            #amount = what we are expecting
            message = {"message": "Payment was received, but the amount is not correct"}
            
            if amount >=2500:
                #import math module at the top
                total = math.cell((amount+100)/(1-0.015))
            else: 
                total = math.cell((amount)/(1-0.015));

            #if the amount coming from paystack and what we have calculated from the database are equal 
            if total == paystacktotal:
                #update cart(paid=True)
                c = CartSerializer(data={"paid":True}, instance=cart, partial=True)   
                if c.is_valid():
                    c.save()
                    message = {"message": response["message"]}
                return Response(message)
        else:
            return Response(response)            
    
class DeliverypointView(viewsets.ModelViewSet):
    serializer_class = DeliverypointSerializer
    queryset = Deliverypoint.objects.all()
    

