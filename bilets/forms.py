from django import forms
from .models import Passenger, Ticket

class TicketSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Поиск')
    transport_type = forms.ChoiceField(choices=[('','Любой'),('air','Авиа'),('rail','ЖД')], required=False, label='Тип')
    origin = forms.CharField(max_length=100, required=False, label='Откуда')
    destination = forms.CharField(max_length=100, required=False, label='Куда')
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}), label='Дата с')
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}), label='Дата по')
    price_min = forms.DecimalField(required=False, min_value=0, label='Цена от')
    price_max = forms.DecimalField(required=False, min_value=0, label='Цена до')

class BookingForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'email']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['transport_type','origin','destination','departure_date','price','image']
        widgets = {'departure_date': forms.DateInput(attrs={'type':'date'})}
