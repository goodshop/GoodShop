from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth import login
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from .forms import CustomerForm
from .models import CustomerProfile
from goodshop.models import Category, Phone


## Helper Functions
from goodshop.utils import add_user_context, search_products

## Views

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