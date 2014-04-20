from django.db import models
from django.contrib.auth.models import User

from django.utils.encoding import smart_unicode

class CustomerProfile(models.Model):
    ''''''
    user = models.OneToOneField(User)
    address = models.CharField(max_length=120,
                            null=False,
                            blank=False,
                            verbose_name="Address"
                            )
    def get_name(self):
        return self.user.first_name + self.user.last_name

    def __unicode__(self):
        return smart_unicode("%s, %s" % (self.get_name(), self.user.email))

class VendorProfile(models.Model):
    ''''''
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
        return self.user.first_name + self.user.last_name

    def __unicode__(self):
        return smart_unicode("%s, %s" % (self.get_name(), self.user.email))

class Phone(models.Model):
    ''' Relates a user with a phone number
    This is used by both customers and vendors.
    '''
    user = models.ForeignKey(User)
    phone = models.IntegerField(verbose_name="Phone number")
    def __unicode__(self):
        return smart_unicode(str(self.phone))


class Category(models.Model):
    '''Names of categories'''
    name = models.CharField(max_length=120,
                            null=False,
                            blank=False,
                            verbose_name="Category"
                            )
    def __unicode__(self):
        return smart_unicode(self.name)


class Product(models.Model):
    '''Product that is related to a category and a vendor'''
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
    '''An order is related to a client. The time stamp of the purchase
    is registered and the total price of the order as it was at the time
    of the purchase, since the prices of the products may change at any time
    '''
    client = models.ForeignKey(User)
    product = models.ManyToManyField(Product, through='ProductInOrder')
    purachase_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)


class ProductImage(models.Model):
    '''A one to many relation, between images and a product'''
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='products')

    def __unicode__(self):
        return smart_unicode(self.product.name)

    def get_img_url(self):
        return 'http://localhost:8000/media/%s' % self.image


class ProductInOrder(models.Model):
    '''
    The ProductInOrder model represents information about a specific
    product ordered by a customer. The price is stored with the value
    they had at the time of the order.
    '''
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()