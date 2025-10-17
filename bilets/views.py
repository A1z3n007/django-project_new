from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Ticket, Booking, Passenger
from .forms import TicketSearchForm, BookingForm, TicketForm

def is_staff(user):
    return user.is_staff

def list_view(request):
    form = TicketSearchForm(request.GET or None)
    qs = Ticket.objects.all().order_by('departure_date')
    if form.is_valid():
        q = form.cleaned_data.get('q')
        tt = form.cleaned_data.get('transport_type')
        origin = form.cleaned_data.get('origin')
        dest = form.cleaned_data.get('destination')
        dfrom = form.cleaned_data.get('date_from')
        dto = form.cleaned_data.get('date_to')
        pmin = form.cleaned_data.get('price_min')
        pmax = form.cleaned_data.get('price_max')

        if q:
            qs = qs.filter(origin__icontains=q) | qs.filter(destination__icontains=q)
        if tt: qs = qs.filter(transport_type=tt)
        if origin: qs = qs.filter(origin__icontains=origin)
        if dest: qs = qs.filter(destination__icontains=dest)
        if dfrom: qs = qs.filter(departure_date__gte=dfrom)
        if dto: qs = qs.filter(departure_date__lte=dto)
        if pmin is not None: qs = qs.filter(price__gte=pmin)
        if pmax is not None: qs = qs.filter(price__lte=pmax)

    paginator = Paginator(qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params = request.GET.copy()
    params.pop('page', None)
    qs_no_page = params.urlencode()
    return render(request, 'bilets/list.html', {
        'form': form,
        'page_obj': page_obj,
        'tickets': page_obj.object_list,
        'qs_no_page': qs_no_page,
    })

def detail_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'bilets/detail.html', {'ticket': ticket})

def book_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            passenger, _ = Passenger.objects.get_or_create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
            )
            booking = Booking.objects.create(
                ticket=ticket,
                passenger=passenger,
                user=request.user if request.user.is_authenticated else None,
                paid=False
            )
            messages.success(request, f'Бронь оформлена! Номер: {booking.id}')
            return redirect('bilets:booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'bilets/book.html', {'ticket': ticket, 'form': form})

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'bilets/booking_success.html', {'booking': booking})

def booking_mark_paid(request, booking_id):
    if request.method != 'POST':
        return redirect('bilets:booking_success', booking_id=booking_id)
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.paid = True
    booking.save(update_fields=['paid'])
    messages.success(request, 'Оплата помечена как успешная (учебный режим).')
    return redirect('bilets:booking_success', booking_id=booking.id)

@login_required
@user_passes_test(is_staff)
def ticket_add(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            t = form.save()
            messages.success(request, f'Билет #{t.id} создан.')
            return redirect('bilets:detail', pk=t.id)
    else:
        form = TicketForm()
    return render(request, 'bilets/ticket_form.html', {'form': form, 'title': 'Новый билет'})
