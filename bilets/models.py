from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    TYPE_CHOICES = [('air','Авиа'), ('rail','ЖД')]
    transport_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='air')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='tickets/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_transport_type_display()} {self.origin} → {self.destination} {self.departure_date}"

class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Booking(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ticket_bookings')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Бронь #{self.id} — {self.passenger} — {self.ticket}"
