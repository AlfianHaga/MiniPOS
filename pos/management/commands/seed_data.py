from django.core.management.base import BaseCommand
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import random

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
    help = "Seed the database with sample data for all models."

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write("Clearing existing data...")
        PurchaseOrderItem.objects.all().delete()
        PurchaseOrder.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Customer.objects.all().delete()
        Supplier.objects.all().delete()

        # Create categories
        self.stdout.write("Creating categories...")
        categories_data = [
            {"name": "Minuman", "description": "Berbagai jenis minuman"},
            {"name": "Makanan", "description": "Produk makanan dan snack"},
            {"name": "Alat Tulis", "description": "Perlengkapan tulis menulis"},
            {"name": "Pembersih", "description": "Produk pembersih dan sanitasi"},
        ]
        categories = {}
        for cat_data in categories_data:
            cat = Category.objects.create(**cat_data)
            categories[cat.name] = cat
            self.stdout.write(f"  - {cat.name}")

        # Create suppliers
        self.stdout.write("Creating suppliers...")
        suppliers_data = [
            {
                "name": "PT Maju Jaya",
                "contact_person": "Budi Santoso",
                "phone": "021-5551234",
                "email": "budi@majujaya.com",
                "address": "Jl. Industri No. 10, Jakarta",
            },
            {
                "name": "CV Sumber Rejeki",
                "contact_person": "Siti Aminah",
                "phone": "022-7778888",
                "email": "siti@sumberrejeki.co.id",
                "address": "Jl. Raya Bandung No. 45",
            },
            {
                "name": "UD Berkah Makmur",
                "contact_person": "Ahmad Dahlan",
                "phone": "031-9990000",
                "email": "ahmad@berkahmakmur.com",
                "address": "Jl. Pahlawan No. 88, Surabaya",
            },
        ]
        suppliers = []
        for sup_data in suppliers_data:
            sup = Supplier.objects.create(**sup_data)
            suppliers.append(sup)
            self.stdout.write(f"  - {sup.name}")

        # Create products
        self.stdout.write("Creating products...")
        products_data = [
            {
                "name": "Kopi Kapal Api",
                "category": "Minuman",
                "price": "133424.00",
                "stock": 4,
            },
            {
                "name": "Teh Botol Sosro",
                "category": "Minuman",
                "price": "5000.00",
                "stock": 50,
            },
            {
                "name": "Aqua 600ml",
                "category": "Minuman",
                "price": "3500.00",
                "stock": 100,
            },
            {
                "name": "Indomie Goreng",
                "category": "Makanan",
                "price": "3000.00",
                "stock": 75,
            },
            {"name": "Chitato", "category": "Makanan", "price": "8500.00", "stock": 30},
            {"name": "Oreo", "category": "Makanan", "price": "12000.00", "stock": 25},
            {
                "name": "Pensil 2B",
                "category": "Alat Tulis",
                "price": "2000.00",
                "stock": 60,
            },
            {
                "name": "Buku Tulis",
                "category": "Alat Tulis",
                "price": "5000.00",
                "stock": 40,
            },
            {
                "name": "Pulpen Pilot",
                "category": "Alat Tulis",
                "price": "3500.00",
                "stock": 55,
            },
            {
                "name": "Sabun Cuci Piring",
                "category": "Pembersih",
                "price": "15000.00",
                "stock": 20,
            },
            {
                "name": "Tisu Paseo",
                "category": "Pembersih",
                "price": "18000.00",
                "stock": 15,
            },
        ]
        products = []
        for prod_data in products_data:
            cat_name = prod_data.pop("category")
            prod_data["category"] = categories[cat_name]
            prod = Product.objects.create(**prod_data)
            products.append(prod)
            self.stdout.write(f"  - {prod.name} (Stok: {prod.stock})")

        # Create customers
        self.stdout.write("Creating customers...")
        customers_data = [
            {
                "name": "Andi Wijaya",
                "phone": "081234567890",
                "address": "Jl. Merdeka No. 10, Jakarta",
            },
            {
                "name": "Budi Hartono",
                "phone": "082345678901",
                "address": "Jl. Sudirman No. 25, Bandung",
            },
            {
                "name": "Citra Dewi",
                "phone": "083456789012",
                "address": "Jl. Gatot Subroto No. 15, Surabaya",
            },
            {
                "name": "Dedi Kusuma",
                "phone": "084567890123",
                "address": "Jl. Ahmad Yani No. 30, Semarang",
            },
            {
                "name": "Eka Putri",
                "phone": "085678901234",
                "address": "Jl. Diponegoro No. 5, Yogyakarta",
            },
        ]
        customers = []
        for cust_data in customers_data:
            cust = Customer.objects.create(**cust_data)
            customers.append(cust)
            self.stdout.write(f"  - {cust.name}")

        # Create purchase orders
        self.stdout.write("Creating purchase orders...")
        for i in range(3):
            supplier = random.choice(suppliers)
            po = PurchaseOrder.objects.create(
                supplier=supplier,
                order_number=f"PO-2024{str(i+1).zfill(3)}",
                status="received" if i < 2 else "pending",
                total_amount=Decimal("0"),
                notes=f"Pembelian rutin bulan ini dari {supplier.name}",
                order_date=timezone.now() - timedelta(days=random.randint(1, 10)),
            )

            if po.status == "received":
                po.received_date = po.order_date + timedelta(days=random.randint(1, 3))
                po.save()

            # Add items to PO
            num_items = random.randint(2, 4)
            po_total = Decimal("0")
            selected_products = random.sample(products, num_items)

            for prod in selected_products:
                qty = random.randint(10, 50)
                unit_price = Decimal(str(prod.price))

                PurchaseOrderItem.objects.create(
                    purchase_order=po,
                    product=prod,
                    quantity=qty,
                    unit_price=unit_price,
                )
                po_total += qty * unit_price

            po.total_amount = po_total
            po.save()
            self.stdout.write(f"  - {po.order_number} ({po.status})")

        # Create orders with some items having discounts
        self.stdout.write("Creating orders...")
        for i in range(10):
            customer = random.choice(customers)
            order = Order.objects.create(
                customer=customer,
                total_price=Decimal("0"),
                created_at=timezone.now() - timedelta(days=random.randint(0, 7)),
            )

            # Add items to order
            num_items = random.randint(1, 4)
            order_total = Decimal("0")
            selected_products = random.sample(
                [p for p in products if p.stock > 0],
                min(num_items, len([p for p in products if p.stock > 0])),
            )

            for prod in selected_products:
                qty = random.randint(1, min(3, prod.stock))
                discount = Decimal(
                    random.choice([0, 0, 0, 5, 10, 15])
                )  # Most items no discount

                item = OrderItem.objects.create(
                    order=order,
                    product=prod,
                    quantity=qty,
                    price=Decimal(str(prod.price)),
                    discount_percent=discount,
                )
                order_total += item.subtotal()

            order.total_price = order_total
            order.save()
            self.stdout.write(
                f"  - Order #{order.id} - {customer.name} (Rp {order_total:,.0f})"
            )

        self.stdout.write(self.style.SUCCESS("\n✓ Database seeded successfully!"))
        self.stdout.write(f"  Categories: {Category.objects.count()}")
        self.stdout.write(f"  Suppliers: {Supplier.objects.count()}")
        self.stdout.write(f"  Products: {Product.objects.count()}")
        self.stdout.write(f"  Customers: {Customer.objects.count()}")
        self.stdout.write(f"  Purchase Orders: {PurchaseOrder.objects.count()}")
        self.stdout.write(f"  Orders: {Order.objects.count()}")
