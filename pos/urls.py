from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("clear-cache/", views.clear_cache_page, name="clear_cache"),
    path("", views.dashboard, name="dashboard"),
    path("low-stock/", views.low_stock_products, name="low_stock_products"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/import/", views.product_import, name="product_import"),
    path(
        "products/import/template/",
        views.product_import_template,
        name="product_import_template",
    ),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/add/", views.customer_create, name="customer_create"),
    path("customers/<int:pk>/edit/", views.customer_update, name="customer_update"),
    path("customers/<int:pk>/delete/", views.customer_delete, name="customer_delete"),
    path("suppliers/", views.supplier_list, name="supplier_list"),
    path("suppliers/add/", views.supplier_create, name="supplier_create"),
    path("suppliers/<int:pk>/edit/", views.supplier_update, name="supplier_update"),
    path("suppliers/<int:pk>/delete/", views.supplier_delete, name="supplier_delete"),
    path("purchase-orders/", views.purchase_order_list, name="purchase_order_list"),
    path(
        "purchase-orders/create/",
        views.purchase_order_create,
        name="purchase_order_create",
    ),
    path(
        "purchase-orders/<int:pk>/",
        views.purchase_order_detail,
        name="purchase_order_detail",
    ),
    path(
        "purchase-orders/<int:pk>/receive/",
        views.purchase_order_receive,
        name="purchase_order_receive",
    ),
    path("orders/", views.orders_list, name="orders_list"),
    path("orders/create/", views.order_create, name="order_create"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("orders/<int:pk>/receipt/", views.order_receipt, name="order_receipt"),
    path("reports/", views.reports, name="reports"),
    path("reports/export/pdf/", views.report_export_pdf, name="report_export_pdf"),
    path(
        "reports/export/excel/", views.report_export_excel, name="report_export_excel"
    ),
    path("analytics/", views.analytics, name="analytics"),
    path("backups/", views.backups_list, name="backups_list"),
    path(
        "backups/download/<str:filename>/",
        views.backup_download,
        name="backup_download",
    ),
]
