from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def home(request):
    return render(request, 'main/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

@login_required
def profile(request):
    from bilets.models import Booking
    from marketplace.models import Order

    # --- фильтры из GET ---
    order_status = request.GET.get('order_status')  # '', 'paid', ...
    bookings_paid = request.GET.get('bookings_paid')  # '', 'yes', 'no'

    orders_qs = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-id')
    if order_status:
        orders_qs = orders_qs.filter(status=order_status)

    bookings_qs = Booking.objects.filter(user=request.user).select_related('ticket', 'passenger').order_by('-id')
    if bookings_paid == 'yes':
        bookings_qs = bookings_qs.filter(paid=True)
    elif bookings_paid == 'no':
        bookings_qs = bookings_qs.filter(paid=False)

    # --- пагинация (раздельная) ---
    orders_paginator = Paginator(orders_qs, 5)
    bookings_paginator = Paginator(bookings_qs, 5)
    page_orders = request.GET.get('page_orders')
    page_bookings = request.GET.get('page_bookings')

    orders_page = orders_paginator.get_page(page_orders)
    bookings_page = bookings_paginator.get_page(page_bookings)

    ctx = {
        'orders_page': orders_page,
        'bookings_page': bookings_page,
        'order_status': order_status or '',
        'bookings_paid': bookings_paid or '',
    }
    return render(request, 'main/profile.html', ctx)
