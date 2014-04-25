from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth import login
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from .forms import CustomerForm
from .models import CustomerProfile
from goodshop.models import Phone, Product, Order, ProductInOrder

## Shopping Cart
from .cart import Cart, Item, manage_cart, get_shopping_cart, update_shopping_cart

## Helper Functions
from goodshop.utils import add_user_context, search_products, get_categories

# E-mail
from .email import email_order_notification


## Views
def customer_home(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    if request.method == 'POST' and request.POST:
        print request.POST['search']

    categories = get_categories()
    context = kwargs.pop('context', '')
    name = kwargs.pop('name', '')

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

    action = kwargs.pop('action', '')
    redirect_url = manage_cart(request, action)
    return HttpResponseRedirect(redirect_url)

def order_manager(request):
    cart = get_shopping_cart(request)
    if not cart.is_empty():
        # Create the order
        order = Order.objects.create(
                    customer=request.user,
                    total_price=cart.total()
                )
        order.save()

        for item in cart:
            product_in_order = ProductInOrder.objects.create(
                                order=order,
                                product=item.product,
                                unit_price=item.product.price,
                                total_price=item.total(),
                                quantity=item.quantity
                            )
            product_in_order.save()

        cart.empty()
        update_shopping_cart(request, cart)

        ## Send notifications
        email_order_notification(order)

    return reverse_lazy('customer_home')

def cart_checkout(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    redirect_url = order_manager(request)

    return HttpResponseRedirect(redirect_url)


def my_orders(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    orders = Order.objects.filter(customer=request.user).order_by('-purchase_date', 'total_price')

    return render_to_response("customer/orders.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )

def view_order(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    order_id = kwargs.pop('order_id','')

    if order_id:
        orders = Order.objects.filter(pk=order_id, customer=request.user)

        if not orders:
            return HttpResponseRedirect(reverse_lazy('my_orders'))

        order = orders[0]
        products = order.get_order_products()
        sales = order.sales()

    return render_to_response("customer/view_order.html",
                             locals(),
                             context_instance=RequestContext(request)
                             )

# Registration Form
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