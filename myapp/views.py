
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import stripe
import json

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import Q, F

from myapp.models import(
    Product,
    Cart, 
    Wishlist, 
    Order, 
    Payment
)
from myapp.serializers import (ProductSerializer, 
    CartSerializer,
    WishlistSerializer, 
    OrderSerializer
    )



stripe.api_key = settings.STRIPE_SECRET_KEY

class productlist(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
   
class cartlist(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, selling_price = serializer.validated_data['product'].price) 
    
  
class wishlistView(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user,price = serializer.validated_data['product'].price)
    
    
    
"""request.user id will be hard coded because the usage of POST man tool"""



class create_checkout_session(APIView):
    query_set = Payment
    def post(self, request, format=None):
        domain_url = 'http://localhost:8000/'
        
        cart_product = Cart.objects.filter(
                Q(user_id= 1) & Q(is_active=True))
        
        
        total_price = Cart.objects.filter(Q(user = User.objects.get(id = 1)) & Q(
             is_active=True)).aggregate(tot=Sum(F('selling_price') * F('quantity')))
        print(total_price)
        
        o = Order.objects.create(order_status = 2, order_user_id = User.objects.get(id = 1).id, total_order_amount = 0)
        o.product.add(*cart_product)
        
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            success_url = domain_url,
            cancel_url = domain_url,
            payment_method_types=['card'],
            line_items=[
                    {
                        'price_data': {
                            'unit_amount': int(total_price['tot']),
                            'currency': 'inr',
                            'product_data': {'name': 'Mobile'},
                        },
                        'quantity': 1,
                    }
                ],
            metadata = {"order_id": o.id},
            mode='payment',
        )
        print(checkout_session)
        return Response(status=status.HTTP_200_OK,data = checkout_session.url)
    
    
class webhook_success(APIView):
    def post(self, request, format=None):
        payload = request.body.decode('utf-8')
        endpoint_secret = settings.STRIPE_SECRET_KEY 
        event = json.loads(payload)
        
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            transaction_id = session['id']
            print(transaction_id)
            customer_email = session['customer_details']['email']
            order_id = event['data']['object']["metadata"]["order_id"]
            amount = event['data']['object']["amount_total"]
            print('Payment successfull')
            o = Order.objects.filter(id = order_id).update(order_status = 1, total_order_amount = amount)
            Cart.objects.filter(user = 1).update(is_active = False)
            Payment.objects.create(transactionid = transaction_id,  paid_status = True, amount = session['amount_total'], email =  customer_email, order = Order.objects.get(id = order_id))
        
        elif  event['type'] == "payment_intent.payment_failed":
            session = event['data']['object']
            transaction_id = session['id']
            amount = event['data']['object']["amount_total"]
            customer_email = session['billing_details']['email']
            print('Payment Failed')

        return Response(status=status.HTTP_200_OK)

