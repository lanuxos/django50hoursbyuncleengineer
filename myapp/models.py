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


class Category(models.Model):
    catName = models.CharField(max_length=100, default='General')
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.catName


class AllProduct(models.Model):
    catName = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
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


class VerifyEmail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)


class Materials(models.Model):
    name = models.CharField(max_length=100)
    m1 = models.FloatField(null=True, blank=True)
    m2 = models.FloatField(null=True, blank=True)
    m3 = models.FloatField(null=True, blank=True)
    m4 = models.FloatField(null=True, blank=True)
    m5 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    pid = models.CharField(max_length=100, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    pType = models.CharField(max_length=100, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    cycle = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=100, null=True, blank=True)
    notice = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class TestModel(models.Model):
    tid = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=10, null=True, blank=True)
    m1 = models.FloatField(null=True, blank=True)
    m2 = models.FloatField(null=True, blank=True)
    m3 = models.FloatField(null=True, blank=True)
