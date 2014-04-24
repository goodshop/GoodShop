from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth import login
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from .forms import CustomerForm
from .models import CustomerProfile
from goodshop.models import Category, Phone, Product, Order, ProductInOrder

## Helper Functions
import re
import pickle
from goodshop.utils import add_user_context, search_products
# Email
from django.core.mail import send_mail
from project.settings import EMAIL_HOST
class Item(object):
    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity

    def total(self):
        return self.product.price * self.quantity

    def set_qty(self, qty):
        self.quantity = qty if qty >= 1 else 1

    def __str__(self):
        return "%s\tx\t%s\tsub-total: $%s" % (str(self.product), str(self.quantity), str(self.total()))

class Cart(object):
    def __init__(self):
        self.items = list()

    def total(self):
        return sum(map(lambda x: x.quantity * x.product.price,
                       self.items))

    def add_item(self, product, quantity=1):
        if quantity == 0:
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

def get_shopping_cart(request, cart_class=Cart):
    carts = request.session.get('cart', None)
    if carts:
        return pickle.loads(carts)
    return cart_class()

def update_shopping_cart(request, cart):
    request.session['cart'] = pickle.dumps(cart)

def cart_add_product(cart, sku, qty=1):
    prodcut = Product.objects.get(pk=sku)
    cart.add_item(prodcut, qty)

def cart_update_product(cart, sku, qty):
    prodcut = Product.objects.get(pk=sku)
    cart.update_item(prodcut, qty)

def cart_remove_product(cart, sku):
    prodcut = Product.objects.get(pk=sku)
    cart.remove_product(prodcut)

## Views
def customer_home(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    if request.method == 'POST' and request.POST:
        print request.POST['search']

    categories = Category.objects.all()
    context = ''
    name = ''

    if 'context' in kwargs:
        context = kwargs['context']

    if 'name' in kwargs:
        name = kwargs['name']

    products = search_products(context, name)

    actual_category = name if context == 'cat' else ''

    cart = get_shopping_cart(request)
    return render_to_response("customer/home.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )


def shopping_cart(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    cart = get_shopping_cart(request)

    return render_to_response("customer/view_cart.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )


def cart_manager(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    action = kwargs['action']
    cart = get_shopping_cart(request)
    if request.GET and 'sku' in request.GET:
        sku = request.GET['sku']

        if action == 'add-to-cart':
            print "#"*40
            print request
            cart_add_product(cart, sku)
            update_shopping_cart(request, cart)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

        if action == 'remove-from-cart':
            cart_remove_product(cart, sku)
            update_shopping_cart(request, cart)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

        if action == 'remove':
            cart_remove_product(cart, sku)

        if 'qty' in request.GET:
            # Verify numbers only or GTFO
            str_qty = request.GET['qty']
            qty = int(str_qty) if re.match("^[-]*[\d]+$", str_qty) else 0

            if action == 'add':
                cart_add_product(cart, sku, qty=qty)
            elif action == 'update':
                cart_update_product(cart, sku, qty)

    if action == 'clear':
        cart.empty()

    update_shopping_cart(request, cart)
    return HttpResponseRedirect(reverse_lazy('shopping_cart'))


def cart_checkout(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    cart = get_shopping_cart(request)
    if not cart.is_empty():
        # Create the order
        order = Order.objects.create(
                    client=request.user,
                    total_price=cart.total()
                )
        order.save()
        client = CustomerProfile.objects.get(user=order.client)
        for item in cart:
            product_in_order = ProductInOrder.objects.create(
                                order=order,
                                product=item.product,
                                unit_price=item.product.price,
                                total_price=item.total(),
                                quantity=item.quantity
                            )
            product_in_order.save()
            send_mail('Order: #%s from GoodShop' % (order.pk),
                      'OrderNo: #%s\n'
                      'Date: %s\n\n'
                      'Article Details\n\n'
                      '\tProduct: %s\n'
                      '\tQty: %s\n\n'
                      '\tTotal: $%s\n'
                      '\n%s\n\n'
                      'Customer: %s %s\n'
                      '\te-mail: %s\n'
                      '\taddress: %s\n'
                      % (order.pk,
                         order.purachase_date,
                         item.product,
                         item.quantity,
                         item.total(),
                         '-'*70,
                         client.user.first_name, client.user.last_name,
                         client.user.email,
                         client.address
                        ),
                      EMAIL_HOST,
                      [item.product.vendor.email, 'coca_lp@hotmail.com', 'haibrayn@hotmail.com'],
                      fail_silently=False
                      )
        send_mail('[GoodShop] Order created successfully',
                  'OrderNo: #%s\n'
                  'Date: %s\n\t'
                  '%s\n\n'
                  'Total: $%s\n\n'
                  'Thanks!' %
                    (order.pk,
                     order.purachase_date,
                     '\n\t'.join([ str(item) for item in cart]),
                     str(cart.total())
                    ),
                  EMAIL_HOST,
                  [client.user.email, 'coca_lp@hotmail.com', 'haibrayn@hotmail.com'],
                  fail_silently=False
                  )
        cart.empty()
        update_shopping_cart(request, cart)

    return HttpResponseRedirect(reverse_lazy('customer_home'))

class CustomerRegistration(FormView):
    template_name = 'registration/customer_registration.html'
    form_class = CustomerForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        user = form.save()

        profile = CustomerProfile(user=user)
        profile.address = form.cleaned_data['address']
        profile.save()

        phone = Phone(user=user)
        phone.phone = form.cleaned_data['phone']
        phone.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return super(CustomerRegistration, self).form_valid(form)