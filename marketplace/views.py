from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from .models import Product, Category, Order, OrderItem
from .forms import CartAddForm, ProductFilterForm, ProductForm
from .cart import add_to_cart, remove_from_cart, get_cart, clear_cart

def is_staff(user):
    return user.is_staff

def product_list(request):
    category_slug = request.GET.get('category')
    qs = Product.objects.filter(in_stock=True).select_related('category')
    categories = Category.objects.all()

    fform = ProductFilterForm(request.GET or None)
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if fform.is_valid():
        q = fform.cleaned_data.get('q')
        pmin = fform.cleaned_data.get('price_min')
        pmax = fform.cleaned_data.get('price_max')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
        if pmin is not None:
            qs = qs.filter(price__gte=pmin)
        if pmax is not None:
            qs = qs.filter(price__lte=pmax)

    paginator = Paginator(qs.order_by('id'), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ---- Сформировать querystring без параметра page ----
    params = request.GET.copy()
    params.pop('page', None)
    qs_no_page = params.urlencode()

    return render(request, 'marketplace/product_list.html', {
        'products': page_obj.object_list,
        'categories': categories,
        'active_category': category_slug,
        'page_obj': page_obj,
        'filter_form': fform,
        'qs_no_page': qs_no_page,  # <-- используем в шаблоне
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = CartAddForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        add_to_cart(request, product.id, form.cleaned_data['quantity'])
        messages.success(request, f'Добавлено в корзину: {product.title}')
        return redirect('marketplace:cart_view')
    return render(request, 'marketplace/product_detail.html', {'product': product, 'form': form})

def cart_view(request):
    cart = get_cart(request)
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)
    items = []
    total = 0
    for p in products:
        qty = cart.get(str(p.id), 0)
        subtotal = p.price * qty
        total += subtotal
        items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
    return render(request, 'marketplace/cart.html', {'items': items, 'total': total})

def cart_remove(request, pk):
    remove_from_cart(request, pk)
    messages.info(request, 'Товар удалён из корзины.')
    return redirect('marketplace:cart_view')

def checkout(request):
    if request.method == 'POST':
        cart = get_cart(request)
        if not cart:
            messages.info(request, 'Корзина пуста.')
            return redirect('marketplace:product_list')

        order = Order.objects.create(user=request.user if request.user.is_authenticated else None)
        products = Product.objects.filter(id__in=[int(k) for k in cart.keys()])
        for p in products:
            qty = cart[str(p.id)]
            OrderItem.objects.create(order=order, product=p, price=p.price, quantity=qty)

        order.status = 'paid'
        order.save(update_fields=['status'])
        clear_cart(request)
        messages.success(request, f'Заказ #{order.id} оплачен (учебный режим).')
        return redirect('marketplace:order_detail', pk=order.id)

    return render(request, 'marketplace/checkout.html')

def checkout_success(request):
    return render(request, 'marketplace/checkout_success.html')

def checkout_cancel(request):
    return render(request, 'marketplace/checkout_cancel.html')

def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), pk=pk)
    # Подготовим строки с подсчитанным subtotal, чтобы не мудрить в шаблоне
    rows = []
    for it in order.items.all():
        rows.append({
            'title': it.product.title,
            'price': it.price,
            'quantity': it.quantity,
            'subtotal': it.price * it.quantity,
        })
    return render(request, 'marketplace/order_detail.html', {'order': order, 'rows': rows})

@login_required
@user_passes_test(is_staff)
def order_change_status(request, pk, new_status):
    order = get_object_or_404(Order, pk=pk)
    allowed = dict(Order.STATUS_CHOICES).keys()
    if new_status not in allowed:
        raise Http404("Unknown status")
    order.status = new_status
    order.save(update_fields=['status'])
    messages.success(request, f'Статус заказа #{order.id} изменён на «{order.get_status_display()}».')
    return redirect('marketplace:order_detail', pk=order.id)

@login_required
@user_passes_test(is_staff)
def order_pdf(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=order_{order.id}.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    x, y = 20*mm, height - 20*mm

    p.setFont("Helvetica-Bold", 14)
    p.drawString(x, y, f"Заказ #{order.id}")
    y -= 8*mm
    p.setFont("Helvetica", 11)
    p.drawString(x, y, f"Статус: {order.get_status_display()}   Дата: {order.created_at.strftime('%d.%m.%Y %H:%M')}")
    y -= 10*mm

    p.setFont("Helvetica-Bold", 11)
    p.drawString(x, y, "Позиции:")
    y -= 6*mm
    p.setFont("Helvetica", 10)
    for it in order.items.all():
        line = f"- {it.product.title}  ×{it.quantity}  —  {it.price} ₸  (= {it.price * it.quantity} ₸)"
        p.drawString(x, y, line)
        y -= 6*mm
        if y < 20*mm:
            p.showPage()
            y = height - 20*mm
            p.setFont("Helvetica", 10)

    y -= 6*mm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, f"Итого: {order.total_amount} ₸")

    p.showPage()
    p.save()
    return response

@login_required
@user_passes_test(is_staff)
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save()
            messages.success(request, f'Товар «{prod.title}» создан.')
            return redirect('marketplace:product_detail', pk=prod.id)
    else:
        form = ProductForm()
    return render(request, 'marketplace/product_form.html', {'form': form, 'title': 'Новый товар'})
