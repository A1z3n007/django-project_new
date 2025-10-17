CART_SESSION_KEY = 'cart'

def get_cart(request):
    return request.session.setdefault(CART_SESSION_KEY, {})

def add_to_cart(request, product_id, quantity=1):
    cart = get_cart(request)
    cart[str(product_id)] = cart.get(str(product_id), 0) + int(quantity)
    request.session.modified = True

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    request.session.modified = True

def clear_cart(request):
    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True
