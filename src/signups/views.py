from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from .forms import SignUpForm, CustomerForm, VendorForm
from .models import ClientProfile, VendorProfile

def add_user_context(request):
    request.customer = ClientProfile.objects.filter(user=request.user)
    request.vendor = VendorProfile.objects.filter(user=request.user)

class CustomerRegistration(FormView):
    template_name = 'registration/customer_registration.html'
    form_class = CustomerForm
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user = form.save()
        profile = ClientProfile(user=user)
        profile.address = form.cleaned_data['address']
        profile.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return super(CustomerRegistration, self).form_valid(form)

class VendorRegistration(FormView):
    template_name = 'registration/vendor_registration.html'
    form_class = VendorForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        profile = VendorProfile(user=user)
        profile.address = form.cleaned_data['address']
        profile.payment = form.cleaned_data['payment']
        profile.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return super(VendorRegistration, self).form_valid(form)


def home(request):
    cosito = ['hola',12,'yoyo']
    tabla = [1,2,3]
    add_user_context(request)
    return render_to_response("home.html",
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