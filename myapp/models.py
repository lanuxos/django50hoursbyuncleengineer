from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photoProfile',
                              null=True, blank=True, default='default.jpg')
    userType = models.CharField(max_length=100, default='member')
    cartQuantity = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class AllProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    detail = models.TextField(null=True, blank=True)
    imageUrl = models.CharField(max_length=200, null=True, blank=True)
    inStock = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=200, default='-')
    image = models.ImageField(upload_to="products", null=True, blank=True)

    def __str__(self):  # to show the name of products on database instead of object number
        return self.name + ' (' + str(self.quantity) + ')'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productId = models.CharField(max_length=100)
    productName = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.productName + ' (' + self.user.first_name + ' ' + self.user.last_name + ': ' + str(self.quantity) + ')'


class OrderList(models.Model):
    orderId = models.CharField(max_length=100)
    productId = models.CharField(max_length=100)
    productName = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()


class OrderPending(models.Model):
    orderId = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    address = models.TextField()
    shipping = models.CharField(max_length=100)
    payment = models.CharField(max_length=100)
    other = models.TextField(null=True, blank=True)
    stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    paid = models.BooleanField(default=False)
    slip = models.ImageField(upload_to="slip", null=True, blank=True)
    slipTime = models.CharField(max_length=100, null=True, blank=True)
    paymentId = models.CharField(max_length=100, null=True, blank=True)
    trackingNumber = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.orderId
