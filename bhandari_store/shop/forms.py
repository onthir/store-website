from django import forms
from .models import *
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'stocks', 'cost_price', 'selling_price', 'exipry_date',)

class UpdatenameForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name',)

class PriceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('cost_price', 'selling_price')