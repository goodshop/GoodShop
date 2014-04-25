from django.core.urlresolvers import reverse_lazy

import re
import pickle

from goodshop.models import Product

class Item(object):
    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity

    def total(self):
        return self.product.price * self.quantity

    def set_qty(self, qty):
        self.quantity = qty if qty >= 1 else 1

    def __str__(self):
        return "%s\tx\t%s\tsub-total: $%s" % (self.quantity, self.product, str(self.total()))

class Cart(object):
    def __init__(self):
        self.items = list()

    def total(self):
        return sum(map(lambda x: x.quantity * x.product.price,
                       self.items))

    def add_item(self, product, quantity=1):
        if quantity == 0 or not product.stock:
            return
        if self.has_product(product):
            index = self.get_product_index(product)
            new_val = self.items[index].quantity + quantity
            self.items[index].set_qty(new_val)
        elif quantity >= 1:
            item = Item(product, quantity)
            self.items.append(item)

    def update_item(self, product, quantity):
        if quantity < 1:
            return
        if self.has_product(product):
            index = self.get_product_index(product)
            self.items[index].quantity = quantity
        else:
            raise Exception("Can't update unexistent product")

    def is_empty(self):
        return self.items == []

    def empty(self):
        self.items = list()

    def remove_product(self, product):
        self.items = filter(lambda x: x.product.id != product.id, self.items)

    def has_product(self, product):
        for item in self.items:
            if item.product.id == product.id:
                return True
        return False

    def get_product_index(self, product):
        for item in self.items:
            if item.product.id == product.id:
                return self.items.index(item)
        return None

    def get_products(self):
        return ( item.product for item in self.items )

    def __iter__(self):
        return self.forward()

    def forward(self):
        current_index = 0
        while (current_index < len(self.items)):
            item = self.items[current_index]
            current_index += 1
            yield item


# Cart in WSGI Request
def get_shopping_cart(request, cart_class=Cart):
    '''
    Loads a pickled Cart object from the WSGI request session. If there is
    no pickled Cart object, returns a new instance of a Cart.

    Returns Cart object instance.
    '''
    cart_str = request.session.get('cart', None)
    if cart_str:
        return pickle.loads(cart_str)
    return cart_class()

def update_shopping_cart(request, cart):
    '''
    Creates a pickled Cart instance and stores it into the
    WSGI request session.
    '''
    request.session['cart'] = pickle.dumps(cart)


# Manage products in cart
def cart_add_product(cart, sku, qty=1):
    prodcut = Product.objects.get(pk=sku)
    cart.add_item(prodcut, qty)

def cart_update_product(cart, sku, qty):
    prodcut = Product.objects.get(pk=sku)
    cart.update_item(prodcut, qty)

def cart_remove_product(cart, sku):
    prodcut = Product.objects.get(pk=sku)
    cart.remove_product(prodcut)


# Manage cart requests
def manage_cart(request, action):
    '''
    Manages the cart obtained from the wsgirequest and
    returns a string containing the url to redirect the view
    '''
    cart = get_shopping_cart(request)

    str_qty = request.GET.get('qty', '')
    sku = request.GET.get('sku', '')

    if sku:
        if action == 'add-to-cart':
            cart_add_product(cart, sku)
            update_shopping_cart(request, cart)
            return request.META.get('HTTP_REFERER', reverse_lazy('customer_home'))

        if action == 'remove-from-cart':
            cart_remove_product(cart, sku)
            update_shopping_cart(request, cart)
            return request.META.get('HTTP_REFERER', reverse_lazy('customer_home'))

        if action == 'remove':
            cart_remove_product(cart, sku)

        if str_qty:
            # Verify numbers only or GTFO
            qty = int(str_qty) if re.match("^[-]*[\d]+$", str_qty) else 0

            if action == 'add':
                cart_add_product(cart, sku, qty=qty)
            elif action == 'update':
                cart_update_product(cart, sku, qty)

    if action == 'clear':
        cart.empty()

    update_shopping_cart(request, cart)
    return reverse_lazy('shopping_cart')
