from django.urls import path, include
from myapp.views import productlist, cartlist, wishlistView, test_payment, orderplaced, payment, webhook_success
from myapp.views import get_api_stripe_key

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'product',productlist)
router.register(r'cart', cartlist)
router.register(r'wishlist', wishlistView)

urlpatterns = [
    
    path('', include(router.urls)),
    path('key/', get_api_stripe_key),
    path('test-payment/', test_payment),
    path('order/',orderplaced.as_view()),
    path('payment/', payment.as_view()),
    
    
    path('webhook/', webhook_success.as_view()),
    
]
