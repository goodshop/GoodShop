from .customers.models import CustomerProfile
from .vendors.models import VendorProfile
from .models import Category, Product

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
