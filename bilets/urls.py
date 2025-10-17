from django.urls import path
from . import views

app_name = 'bilets'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('<int:pk>/', views.detail_view, name='detail'),
    path('<int:pk>/book/', views.book_view, name='book'),
    path('booking/<int:booking_id>/success/', views.booking_success, name='booking_success'),

    path('booking/<int:booking_id>/mark_paid/', views.booking_mark_paid, name='booking_mark_paid'),

    # управление билетами (staff)
    path('manage/ticket/add/', views.ticket_add, name='ticket_add'),
]
