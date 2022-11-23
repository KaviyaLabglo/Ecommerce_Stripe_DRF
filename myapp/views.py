
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import stripe

from django.shortcuts import redirect
from django.conf import settings
import json

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
    
    
@api_view(['GET'])  
def get_api_stripe_key(request):
    pub_key = settings.STRIPE_PUBLIC_KEY 
    secret_key = settings.STRIPE_SECRET_KEY
    return Response ({'Pub_Key':pub_key,'secret_key':secret_key})


@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='pln', 
        payment_method_types=['card'],
        receipt_email='test@example.com')
    print(test_payment_intent)
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


class orderplaced(APIView):
    query_set = Order.objects.all()
    serializer_classes = OrderSerializer
    
    def post(self, request, format=None):
        print(request.data)
        serializer = OrderSerializer(data=request.data)
        #bookserializer = stripe_checkout_SessionSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
           # bookserializer.save(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class payment(APIView):
    query_set = Payment
    def post(self, request, format=None):
        domain_url = 'http://localhost:8000/'
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            success_url=domain_url +'success/',
            cancel_url=domain_url + 'cancelled/',
            payment_method_types=['card'],
            line_items=[
                    {
                        'price_data': {
                            'unit_amount': int(500),
                            'currency': 'inr',
                            'product_data': {'name': 'Mobile'},
                        },
                        'quantity': 1,
                    }
                ],
            
            mode='payment',
        )
        return redirect(checkout_session.url, code = 303)
    
    
class webhook_success(APIView):
    def post(self, request, format=None):
        payload = request.body.decode('utf-8')
        endpoint_secret = settings.STRIPE_SECRET_KEY 
        event = json.loads(payload)
        print(event)
        print("Hoiiiiiiiiiiiiiiiiiiiiiiiiiii")
        print(payload)
        #event = None
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session['customer_details']['email']
            order_id = session['metadata']['order_id']
            print('Payment successfull')
            Payment.objects.create( transaction_id = session["id"],  paid_status = True, amount = 20000, email = customer_email, order = 1)
        return Response(status=status.HTTP_200_OK)

