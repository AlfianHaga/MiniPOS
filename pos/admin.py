from django.contrib import admin
from .models import (
    Product,
    Customer,
    Order,
    OrderItem,
    Category,
    Supplier,
    PurchaseOrder,
    PurchaseOrderItem,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "phone", "email", "created_at")
    search_fields = ("name", "contact_person")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "created_at")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("price",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_price", "created_at")
    inlines = [OrderItemInline]


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "supplier",
        "status",
        "total_amount",
        "order_date",
        "received_date",
    )
    list_filter = ("status",)
    search_fields = ("order_number", "supplier__name")
    inlines = [PurchaseOrderItemInline]
