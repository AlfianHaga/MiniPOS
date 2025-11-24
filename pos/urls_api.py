from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.api_products, name="api_products"),
    path("orders/create/", views.api_create_order, name="api_create_order"),
]
