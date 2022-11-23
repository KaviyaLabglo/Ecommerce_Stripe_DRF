from django.urls import path, include

from myapp.views import (productlist, 
    cartlist, 
    wishlistView, 
    webhook_success, 
    create_checkout_session
)


from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'product',productlist)
router.register(r'cart', cartlist)
router.register(r'wishlist', wishlistView)

urlpatterns = [
    
    path('', include(router.urls)),
   
    path('create_checkout_session/', create_checkout_session.as_view()),
    
    path('webhook/', webhook_success.as_view()),
    
]
