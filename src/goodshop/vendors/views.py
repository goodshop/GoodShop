from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.contrib.auth import login
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

# Create your views here.
from .forms import VendorForm
from .models import VendorProfile
from goodshop.models import Phone
from goodshop.utils import add_user_context

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