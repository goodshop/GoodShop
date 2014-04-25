from django.contrib.auth.models import User

from .models import Category, Product, Phone
from .customers.models import CustomerProfile
from .vendors.models import VendorProfile

## HELPER FUNCTIONS
def add_user_context(request):
    request.customer = False
    request.vendor = False
    if request.user.is_authenticated():
        request.customer = CustomerProfile.objects.filter(user=request.user)
        request.vendor = VendorProfile.objects.filter(user=request.user)

def search_products(context, name):
    if context == 'cat':
        category = Category.objects.get(name=name)
        return Product.objects.filter(category=category)
    elif context == 'search':
        products = Product.objects.filter(id=0)
        for search_name in name.split('-'):
            categories = Category.objects.filter(name__icontains=search_name)
            q = Product.objects.filter(name__icontains=search_name)|Product.objects.filter(category=categories)
            products = products | q
        return products
    return []


def get_categories(name_like=''):
    '''
    Returns all categories or a group of categories filtered
    by a name.
    '''
    if name_like:
        return Category.objects.filter(name__icontains=name_like)
    return Category.objects.all()

## HELPER CLASSES
class Sale(object):
    '''Helper class to store the order products, grouped by vendor'''
    def __init__(self, order, vendor_id, ord_products):
        self.products = ord_products
        self.vendor = User.objects.get(pk=vendor_id)
        self.vendor_phone = Phone.objects.get(user=self.vendor)
        self.vendor_email = self.vendor.email

    def total(self):
        return sum(map(lambda x: x.total_price, self.products))

    def __str__(self):
        return "Phone : %s\ne-mail : %s\n" % (self.vendor_phone, self.vendor_email)

    def __iter__(self):
        return self.forward()

    def forward(self):
        current_index = 0
        while (current_index < len(self.products)):
            product = self.products[current_index]
            current_index += 1
            yield product