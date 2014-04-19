from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from .forms import SignUpForm, CustomerForm, VendorForm
from .models import ClientProfile, VendorProfile, Category, Product, Phone


## HELPER FUNCTIONS
def add_user_context(request):
    request.customer = False
    request.vendor = False
    if request.user.is_authenticated():
        request.customer = ClientProfile.objects.filter(user=request.user)
        request.vendor = VendorProfile.objects.filter(user=request.user)

def search_products(context, name):
    if context == 'cat':
        category = Category.objects.get(name=name)
        return Product.objects.filter(category=category)
    elif context == 'search':
        products = Product.objects.filter(id=0)
        for search_name in name.split('-'):
            categories = Category.objects.filter(name__contains=search_name)
            q = Product.objects.filter(name__contains=search_name)| Product.objects.filter(category=categories)
            products = products | q
        return products
    return []

class CustomerRegistration(FormView):
    template_name = 'registration/customer_registration.html'
    form_class = CustomerForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        user = form.save()

        profile = ClientProfile(user=user)
        profile.address = form.cleaned_data['address']
        profile.save()

        phone = Phone(user=user)
        phone.phone = form.cleaned_data['phone']
        phone.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return super(CustomerRegistration, self).form_valid(form)

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


## Redirect to login or a vendor or customer home page
def home(request):
    add_user_context(request)
    if request.user.is_authenticated():
        if request.vendor:
            return HttpResponseRedirect('/vendor/')
        else:
            return HttpResponseRedirect('/customer/')
    else:
        return HttpResponseRedirect('/login/')


def customer_home(request, *args, **kwargs):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.vendor:
        return HttpResponseRedirect('/vendor/')

    categories = Category.objects.all()
    context = ''
    name = ''

    if 'context' in kwargs:
        context = kwargs['context']

    if 'name' in kwargs:
        name = kwargs['name']

    products = search_products(context, name)

    actual_category = name if context == 'cat' else ''

    return render_to_response("customer/home.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )

def vendor_home(request):
    add_user_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif request.customer:
        return HttpResponseRedirect('/customer/')

    return render_to_response("vendor/home.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )



def thankyou(request, *args, **kwargs):
    form = SignUpForm(request.POST or None)
    add_user_context(request)
    if 'usr' in kwargs:
        usr = kwargs['usr']

    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()
        messages.success(request, 'Conglaturations You Just Joined Something!')
        return HttpResponseRedirect('/thank-you/')

    return render_to_response("thankyou.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )

def aboutus(request):
    add_user_context(request)
    return render_to_response("aboutus.html",
                              locals(),
                              context_instance=RequestContext(request)
                              )