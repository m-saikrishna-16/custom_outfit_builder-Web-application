from django.contrib import admin
from .models import Order, OrderItem,Product

admin.site.register(Product)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'total', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
