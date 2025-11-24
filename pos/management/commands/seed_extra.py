from decimal import Decimal
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from pos.models import (
    Product,
    Customer,
    Category,
    Supplier,
    Order,
    OrderItem,
    PurchaseOrder,
    PurchaseOrderItem,
)


class Command(BaseCommand):
    help = "Add additional demo data (suppliers, purchase orders, orders) without wiping existing records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--suppliers",
            type=int,
            default=5,
            help="Number of suppliers to ensure exist",
        )
        parser.add_argument(
            "--purchase-orders",
            type=int,
            default=5,
            help="Number of purchase orders to create",
        )
        parser.add_argument(
            "--orders", type=int, default=20, help="Number of sales orders to create"
        )
        parser.add_argument(
            "--max-items",
            type=int,
            default=4,
            help="Maximum items per order / purchase order",
        )
        parser.add_argument(
            "--no-purchase",
            action="store_true",
            help="Skip creating purchase orders (only suppliers + sales orders)",
        )

    def handle(self, *args, **options):
        target_suppliers = options["suppliers"]
        target_purchase = options["purchase_orders"]
        target_orders = options["orders"]
        max_items = options["max_items"]
        skip_purchase = options["no_purchase"]

        self.stdout.write("Seeding extra demo data...")

        # Ensure categories and products exist
        if Category.objects.count() == 0 or Product.objects.count() == 0:
            self.stdout.write(
                self.style.ERROR(
                    "Need existing categories and products. Run another seed first."
                )
            )
            return

        # Suppliers
        existing_suppliers = list(Supplier.objects.all())
        supplier_needed = max(0, target_suppliers - len(existing_suppliers))
        for i in range(supplier_needed):
            s = Supplier.objects.create(
                name=f"Supplier Demo {i+1}",
                contact_person=f"CP {i+1}",
                phone=f"08{random.randint(100000000, 999999999)}",
                address=f"Alamat Supplier {i+1}",
            )
            existing_suppliers.append(s)
        self.stdout.write(f"Suppliers now: {len(existing_suppliers)}")

        products = list(Product.objects.all())
        customers = list(Customer.objects.all())
        if not customers:
            self.stdout.write(
                self.style.ERROR("No customers found. Create or seed customers first.")
            )
            return

        # Purchase Orders (increase stock)
        created_po = 0
        if not skip_purchase:
            for i in range(target_purchase):
                supplier = random.choice(existing_suppliers)
                po = PurchaseOrder.objects.create(
                    supplier=supplier,
                    order_number=f"PO-DEMO-{timezone.now().strftime('%Y%m%d')}-{i+1}",
                    status="received",
                    total_amount=Decimal("0"),
                    notes=f"Demo purchase order {i+1}",
                    order_date=timezone.now() - timedelta(days=random.randint(0, 7)),
                )
                po.received_date = po.order_date + timedelta(days=random.randint(0, 2))
                po.save()
                num_items = random.randint(1, max_items)
                chosen = random.sample(products, min(num_items, len(products)))
                po_total = Decimal("0")
                for prod in chosen:
                    qty = random.randint(5, 30)
                    unit_price = prod.price
                    PurchaseOrderItem.objects.create(
                        purchase_order=po,
                        product=prod,
                        quantity=qty,
                        unit_price=unit_price,
                    )
                    po_total += qty * unit_price
                    prod.stock += qty
                    prod.save(update_fields=["stock"])
                po.total_amount = po_total
                po.save(update_fields=["total_amount"])
                created_po += 1
        self.stdout.write(f"Purchase orders created: {created_po}")

        # Sales Orders (decrease stock)
        created_orders = 0
        for i in range(target_orders):
            cust = random.choice(customers)
            order = Order.objects.create(customer=cust, total_price=Decimal("0"))
            num_items = random.randint(1, max_items)
            # pick products with stock
            available = [p for p in products if p.stock > 0]
            if not available:
                break
            chosen = random.sample(available, min(num_items, len(available)))
            order_total = Decimal("0")
            for prod in chosen:
                max_qty = max(1, min(5, prod.stock))
                qty = random.randint(1, max_qty)
                discount = Decimal(random.choice([0, 0, 5, 10, 15]))
                item = OrderItem.objects.create(
                    order=order,
                    product=prod,
                    quantity=qty,
                    price=prod.price,
                    discount_percent=discount,
                )
                order_total += item.subtotal()
                prod.stock -= qty
                prod.save(update_fields=["stock"])
            order.total_price = order_total
            order.save(update_fields=["total_price"])
            created_orders += 1
        self.stdout.write(f"Sales orders created: {created_orders}")

        self.stdout.write(self.style.SUCCESS("Done."))
        self.stdout.write(f"  Categories: {Category.objects.count()}")
        self.stdout.write(f"  Products: {Product.objects.count()}")
        self.stdout.write(f"  Customers: {Customer.objects.count()}")
        self.stdout.write(f"  Suppliers: {Supplier.objects.count()}")
        self.stdout.write(f"  Purchase Orders: {PurchaseOrder.objects.count()}")
        self.stdout.write(f"  Orders: {Order.objects.count()}")
