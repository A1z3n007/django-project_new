from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'in_stock', 'category')
    list_filter = ('in_stock', 'category')
    search_fields = ('title',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')  # <- убрали checkout_session_id
    list_filter = ('status',)
    inlines = [OrderItemInline]
    # readonly_fields = (...)  # <- убрали, чтобы не ссылаться на несуществующие поля
