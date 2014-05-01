from django import forms
from django.contrib.auth.forms import UserCreationForm

from goodshop.models import Product

class VendorForm(UserCreationForm):
    required_css_class = 'form-group'
    address = forms.CharField(required=True)
    payment = forms.CharField(widget=forms.Textarea)
    phone = forms.IntegerField(required=True)

    UserCreationForm.Meta.fields = ('username', 'first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})

class ProductForm(forms.ModelForm):
    required_css_class = 'form-group'
    image = forms.ImageField(required=True)

    class Meta:
        model = Product
        fields = ['category', 'price', 'name']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs.update({'class': 'form-control'})
            self.fields[key].widget.attrs.update({'placeholder': key})