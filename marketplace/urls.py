from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),

    # детальная страница заказа + PDF + смена статуса (staff)
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/<int:pk>/pdf/', views.order_pdf, name='order_pdf'),
    path('order/<int:pk>/status/<str:new_status>/', views.order_change_status, name='order_change_status'),

    # управление товарами (staff)
    path('manage/product/add/', views.product_add, name='product_add'),
]
