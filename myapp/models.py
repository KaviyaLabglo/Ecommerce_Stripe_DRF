from django.db import models
from django.contrib.auth.models import User
# Create your models here.
FAILED = 0
SUCCESS = 1
PENDING = 2
ORDER_STATUS_CHOICES = (
    (SUCCESS, 'Success'),
    (PENDING, 'Pending'),
    (FAILED, 'Cancel')
)


class TimeStampModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(TimeStampModel):
    brand_name = models.CharField(max_length=200)
    brand_logo = models.ImageField(upload_to='image/')
    year = models.IntegerField()
    founder = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.brand_name)


class Product(TimeStampModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/')
    title = models.TextField(max_length=200)
    price = models.IntegerField()
    availability = models.BooleanField(default=False)
    color = models.CharField(max_length=200)

    def __str__(self):
        return "{} {}".format(self.id, self.brand)


class Cart(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    selling_price = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} ".format(self.id)


class Order(TimeStampModel):
    order_user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Cart)
    order_status = models.IntegerField(default=2, choices=ORDER_STATUS_CHOICES)
    total_order_amount = models.IntegerField()

    def __str__(self):
        return "{} {} ".format(self.id, self.order_user, self.order_status)


class Wishlist(TimeStampModel):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    product1 = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    is_active1 = models.BooleanField(default=True)

    def __str__(self):
        return "{} ".format(self.id)
    
class Payment(TimeStampModel):
    transaction_id = models.TextField(max_length=200)
    paid_status =  models.BooleanField(default=False)
    amount = models.IntegerField()
    email = models.EmailField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
   
    