from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SignUp, ClientProfile, VendorProfile

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp

class CustomerForm(UserCreationForm):
    required_css_class = 'form-group'
    address = forms.CharField()
    phone = forms.IntegerField()
    UserCreationForm.Meta.fields = ('username', 'first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})


class VendorForm(UserCreationForm):
    required_css_class = 'form-group'
    address = forms.CharField()
    payment = forms.CharField(widget=forms.Textarea)
    phone = forms.IntegerField()

    UserCreationForm.Meta.fields = ('username', 'first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})
