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

# Email
from django.core.mail import send_mail
from project.settings import EMAIL_HOST
from . import templates

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


def email_order_notification(order):
    sales = order.sales_by_vendor()
    client = order.get_customer_profile()

    ## Info to replace in the templates
    LABELS = {}

    # General order info
    LABELS['order_no'] = order.pk
    LABELS['date'] = order.get_date()
    LABELS['order_total'] = order.total_price

    # Customer info
    LABELS['customer_first_name'] = client.user.first_name
    LABELS['customer_last_name'] = client.user.last_name
    LABELS['customer_phone'] = order.get_customer_phone()
    LABELS['customer_email'] = client.user.email
    LABELS['customer_address'] = client.address

    # Variable info
    LABELS['product_list'] = ''
    LABELS['vendor_first_name'] = ''
    LABELS['vendor_last_name'] = ''


    ## Send vendor e-mail
    for vendor_id in sales:
        ## Variable information in the message
        p_list = order.get_product_report(sales[vendor_id])
        a_prod_in_ord = sales[vendor_id][0]
        vendor = a_prod_in_ord.product.vendor
        vendor_email = vendor.email

        LABELS['product_list'] = p_list.replace('\n', '\n\t')
        LABELS['vendor_first_name'] = vendor.first_name
        LABELS['vendor_last_name'] = vendor.last_name

        send_mail(templates.VENDOR_SUBJECT % (LABELS),
                  templates.VENDOR_MSG     % (LABELS),
                  EMAIL_HOST,
                  [vendor_email, 'coca_lp@hotmail.com', 'haibrayn@hotmail.com'],
                  fail_silently=False
                  )


    ## Send customer e-mail
    order_prods = order.get_order_products()
    p_list = order.get_product_report(order_prods)
    LABELS['product_list'] = p_list.replace('\n', '\n\t')

    send_mail(templates.CUSTOMER_SUBJECT % LABELS,
              templates.CUSTOMER_MSG % LABELS,
              EMAIL_HOST,
              [client.user.email, 'coca_lp@hotmail.com', 'haibrayn@hotmail.com'],
              fail_silently=False
              )

def order_manager(request):
    cart = get_shopping_cart(request)
    if not cart.is_empty():
        # Create the order
        order = Order.objects.create(
                    client=request.user,
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

    orders = Order.objects.filter(client=request.user).order_by('-purachase_date', 'total_price')

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
        orders = Order.objects.filter(pk=order_id, client=request.user)

        if not orders:
            return HttpResponseRedirect(reverse_lazy('my_orders'))

        order = orders[0]
        products = order.get_order_products()
        sales = order.sales_by_vendor()

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