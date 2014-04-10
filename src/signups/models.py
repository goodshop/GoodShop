from django.db import models
from django.contrib.auth.models import User

from django.utils.encoding import smart_unicode


# Create your models here.
class SignUp(models.Model):
    for_you = models.BooleanField(default=True,
                                  verbose_name="Does this make sense to you? If so, check this box.")
    fname = models.CharField(max_length=120,
                             null=True,
                             blank=True,
                             verbose_name="First Name"
                             )
    lname = models.CharField(max_length=120,
                             null=True,
                             blank=True,
                             verbose_name="Last Name"
                             )
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True,
                                     auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,
                                   auto_now=True)

    def __unicode__(self):
        return smart_unicode(self.email)

class ClientProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=120,
                            null=False,
                            blank=False,
                            verbose_name="Address"
                            )
    def get_name(self):
        return self.user.fname + self.user.lname

    def __unicode__(self):
        return smart_unicode("%s, %s" % (self.get_name(), self.user.email))


class VendorProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=120,
                            null=False,
                            blank=False,
                            verbose_name="Address"
                            )
    payment = models.TextField(max_length=120,
                            null=False,
                            blank=False,
                            verbose_name="Address"
                            )

    def get_name(self):
        return self.user.fname + self.user.lname

    def __unicode__(self):
        return smart_unicode("%s, %s" % (self.get_name(), self.user.email))


class Phone(models.Model):
    user = models.ForeignKey(User)
    phone = models.IntegerField()
    def __unicode__(self):
        return smart_unicode(str(self.phone))


class Category(models.Model):
    name = models.CharField(max_length=120,
                            null=False,
                            blank=False,
                            verbose_name="Category"
                            )
    def __unicode__(self):
        return smart_unicode(self.name)


class Product(models.Model):
    category = models.ForeignKey(Category)
    vendor = models.ForeignKey(User)
    name = models.CharField(max_length=120,
                            null=False,
                            blank=False,
                            verbose_name="Product"
                            )
    stock = models.BooleanField(default=True,
                                verbose_name="Have this product in stock")
    def __unicode__(self):
        return smart_unicode(self.name)


class Order(models.Model):
    client = models.ForeignKey(User)
    product = models.ManyToManyField(Product, through='ProductInOrder')
    purachase_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)


class ProductImage(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='products')

    def __unicode__(self):
        return smart_unicode(self.product.name)

    def get_img_url(self):
        return 'http://localhost:8000/media/%s' % self.image


class ProductInOrder(models.Model):
    '''
    The ProductInOrder model represents information about a specific
    product ordered by a customer.
    '''
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
