from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth import login
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from .forms import VendorForm
from .models import VendorProfile
from goodshop.models import Product, Phone, Order, get_orders_for_vendor
from goodshop.utils import add_user_context

def vendor_home(request):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('login'))
    elif request.customer:
        return HttpResponseRedirect(reverse_lazy('customer_home'))
    return HttpResponseRedirect(reverse_lazy('vendor_orders'))


def vendor_orders(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('login'))
    elif request.customer:
        return HttpResponseRedirect(reverse_lazy('customer_home'))

    orders = get_orders_for_vendor(request.user)

    return render_to_response("vendor/orders.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )

def vendor_order(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('login'))
    elif request.customer:
        return HttpResponseRedirect(reverse_lazy('customer_home'))

    order_id = kwargs.pop('order_id','')

    if order_id:
        try:
            order = get_orders_for_vendor(request.user).get(pk=order_id)
        except:
            return HttpResponseRedirect(reverse_lazy('vendor_orders'))
        products = order.get_order_products()
        sale = order.sales(vendor=request.user)

    return render_to_response("vendor/view_order.html",
                             locals(),
                             context_instance=RequestContext(request)
                             )


def my_products(request):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('login'))
    elif request.customer:
        return HttpResponseRedirect(reverse_lazy('customer_home'))
    products = Product.objects.filter(vendor=request.user)
    return render_to_response("vendor/my_products.html",
                             locals(),
                             context_instance=RequestContext(request)
                             )


class VendorRegistration(FormView):
    template_name = 'registration/vendor_registration.html'
    form_class = VendorForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        profile = VendorProfile(user=user)
        profile.address = form.cleaned_data['address']
        profile.payment = form.cleaned_data['payment']
        profile.save()

        phone = Phone(user=user)
        phone.phone = form.cleaned_data['phone']
        phone.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return super(VendorRegistration, self).form_valid(form)