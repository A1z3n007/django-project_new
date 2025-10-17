from django import forms
from .models import Product

class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

class ProductFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Поиск')
    price_min = forms.DecimalField(required=False, min_value=0, label='Цена от')
    price_max = forms.DecimalField(required=False, min_value=0, label='Цена до')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'in_stock', 'image']
