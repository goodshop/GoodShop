from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy

from .utils import add_user_context

# Create your views here.

def home(request):
    '''Redirect to login or a vendor or customer home page'''
    add_user_context(request)
    if request.user.is_authenticated():
        if request.vendor:
            return HttpResponseRedirect('/vendor/')
        else:
            return HttpResponseRedirect('/customer/')

    return HttpResponseRedirect('/login/')


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