from decimal import Decimal
import random
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from pos.models import (
    Product, Customer, Category, Supplier,
    Order, OrderItem, PurchaseOrder, PurchaseOrderItem
)

try:
    from faker import Faker
    try:
        fake = Faker('id_ID')
    except Exception:
        fake = Faker()
except Exception:
    fake = None


class Command(BaseCommand):
    help = 'Seed demo data lengkap: kategori, produk, pelanggan, supplier, purchase orders, sales orders.'

    def add_arguments(self, parser):
        parser.add_argument('--categories', type=int, default=6)
        parser.add_argument('--products', type=int, default=50)
        parser.add_argument('--customers', type=int, default=30)
        parser.add_argument('--suppliers', type=int, default=10)
        parser.add_argument('--purchase-orders', type=int, default=5)
        parser.add_argument('--orders', type=int, default=25)
        parser.add_argument('--max-items', type=int, default=4)
        parser.add_argument('--replace', action='store_true', help='Hapus semua data terkait sebelum seeding')

    def handle(self, *args, **opts):
        cnt_cat = opts['categories']
        cnt_prod = opts['products']
        cnt_cust = opts['customers']
        cnt_sup = opts['suppliers']
        cnt_po = opts['purchase_orders']
        cnt_orders = opts['orders']
        max_items = opts['max_items']
        replace = opts['replace']

        if replace:
            self.stdout.write(self.style.WARNING('Menghapus data lama...'))
            PurchaseOrderItem.objects.all().delete()
            PurchaseOrder.objects.all().delete()
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Customer.objects.all().delete()
            Supplier.objects.all().delete()

        if Category.objects.count() < cnt_cat:
            base_categories = [
                ('Makanan & Minuman', 'Produk konsumsi harian'),
                ('Sembako', 'Kebutuhan pokok'),
                ('Perawatan Diri', 'Kebersihan & personal care'),
                ('Pembersih', 'Produk pembersih rumah'),
                ('Kopi & Teh', 'Minuman hangat'),
                ('Alat Tulis', 'Perlengkapan tulis'),
            ]
            for name, desc in base_categories[:cnt_cat]:
                Category.objects.get_or_create(name=name, defaults={'description': desc})
        categories = list(Category.objects.all())

        need_sup = max(0, cnt_sup - Supplier.objects.count())
        for i in range(need_sup):
            Supplier.objects.create(
                name=f'Supplier Demo {i+1}',
                contact_person=f'CP {i+1}',
                phone=f'08{random.randint(100000000, 999999999)}',
                email=f'supplier{i+1}@example.com',
                address=f'Alamat Supplier {i+1}',
            )
        suppliers = list(Supplier.objects.all())

        prod_names = [
            'Beras Premium','Minyak Goreng','Gula Pasir','Kopi Kapal Api','Teh Celup',
            'Indomie Goreng','Susu UHT','Sabun Mandi','Shampoo Botol','Pasta Gigi',
            'Kecap Manis','Sambal Botol','Detergen Bubuk','Tisu Dapur','Buku Tulis',
            'Pulpen Gel','Pensil HB'
        ]
        need_prod = max(0, cnt_prod - Product.objects.count())
        for i in range(need_prod):
            name = random.choice(prod_names)
            if Product.objects.filter(name=name).exists():
                name = f'{name} {random.randint(1,99)}'
            price = Decimal(random.randint(2000, 150000))
            stock = random.randint(5, 150)
            if fake:
                desc = fake.sentence(nb_words=8)
            else:
                desc = random.choice([
                    'Produk berkualitas untuk kebutuhan harian.',
                    'Produk populer dan banyak dicari.',
                    'Pilihan tepat untuk pelanggan setia.',
                ])
            Product.objects.create(
                name=name,
                category=random.choice(categories),
                price=price,
                stock=stock,
                description=desc
            )
        products = list(Product.objects.all())

        need_cust = max(0, cnt_cust - Customer.objects.count())
        for i in range(need_cust):
            if fake:
                cust_name = fake.name()
                phone = fake.phone_number()
            else:
                cust_name = f'Customer Demo {i+1}'
                phone = f'08{random.randint(100000000,999999999)}'
            Customer.objects.create(name=cust_name, phone=phone)
        customers = list(Customer.objects.all())
        if not customers:
            raise CommandError('Tidak ada customer berhasil dibuat.')

        for i in range(cnt_po):
            supplier = random.choice(suppliers)
            po = PurchaseOrder.objects.create(
                supplier=supplier,
                order_number=f'PO-DEMO-{timezone.now().strftime("%Y%m%d")}-{i+1}',
                status='received',
                total_amount=Decimal('0'),
                notes=f'PO Demo {i+1}',
                order_date=timezone.now() - timedelta(days=random.randint(0, 10)),
            )
            po.received_date = po.order_date + timedelta(days=random.randint(0,3))
            po.save(update_fields=['received_date'])
            num_items = random.randint(1, max_items)
            chosen = random.sample(products, min(num_items, len(products)))
            po_total = Decimal('0')
            for prod in chosen:
                qty = random.randint(5, 40)
                PurchaseOrderItem.objects.create(
                    purchase_order=po,
                    product=prod,
                    quantity=qty,
                    unit_price=prod.price
                )
                po_total += prod.price * qty
                prod.stock += qty
                prod.save(update_fields=['stock'])
            po.total_amount = po_total
            po.save(update_fields=['total_amount'])

        for i in range(cnt_orders):
            cust = random.choice(customers)
            order = Order.objects.create(customer=cust, total_price=Decimal('0'))
            available = [p for p in products if p.stock > 0]
            if not available:
                break
            num_items = random.randint(1, max_items)
            chosen = random.sample(available, min(num_items, len(available)))
            total = Decimal('0')
            for prod in chosen:
                qty = random.randint(1, min(5, prod.stock))
                discount = Decimal(0)
                if random.random() < 0.35:
                    discount = Decimal(random.choice([5,10,15,20]))
                item = OrderItem.objects.create(
                    order=order,
                    product=prod,
                    quantity=qty,
                    price=prod.price,
                    discount_percent=discount
                )
                total += item.subtotal()
                prod.stock -= qty
                prod.save(update_fields=['stock'])
            order.total_price = total
            order.save(update_fields=['total_price'])

        self.stdout.write(self.style.SUCCESS('\n seed_demo_data selesai'))
        self.stdout.write(f'  Kategori: {Category.objects.count()}')
        self.stdout.write(f'  Produk: {Product.objects.count()}')
        self.stdout.write(f'  Pelanggan: {Customer.objects.count()}')
        self.stdout.write(f'  Supplier: {Supplier.objects.count()}')
        self.stdout.write(f'  Purchase Order: {PurchaseOrder.objects.count()}')
        self.stdout.write(f'  Sales Order: {Order.objects.count()}')

