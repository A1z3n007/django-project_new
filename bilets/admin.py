from django.contrib import admin
from .models import Ticket, Passenger, Booking

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id','transport_type','origin','destination','departure_date','price')
    list_filter = ('transport_type','departure_date')
    search_fields = ('origin','destination')

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','email')
    search_fields = ('first_name','last_name','email')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','ticket','passenger','created_at','paid')
    list_filter = ('paid',)
