from decimal import Decimal
import random
from django.core.management.base import BaseCommand

try:
    from faker import Faker

    # Prefer Indonesian locale when available
    try:
        fake = Faker("id_ID")
    except Exception:
        fake = Faker()
except Exception:
    fake = None


class Command(BaseCommand):
    help = "Seed the database with more realistic products, customers and orders."

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories", type=int, default=8, help="Number of categories to create"
        )
        parser.add_argument(
            "--products", type=int, default=30, help="Number of products to create"
        )
        parser.add_argument(
            "--customers", type=int, default=20, help="Number of customers to create"
        )
        parser.add_argument(
            "--orders", type=int, default=50, help="Number of orders to create"
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing products/customers/orders before seeding",
        )

    def handle(self, *args, **options):
        from pos.models import Product, Customer, Order, OrderItem, Category

        cnt_categories = options["categories"]
        cnt_products = options["products"]
        cnt_customers = options["customers"]
        cnt_orders = options["orders"]
        replace = options["replace"]

        self.stdout.write("Seeding realistic data...")

        if replace:
            self.stdout.write(
                "Deleting existing OrderItems, Orders, Products, Customers and Categories..."
            )
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Product.objects.all().delete()
            Customer.objects.all().delete()
            Category.objects.all().delete()

        # Create categories first
        CATEGORIES = [
            ("Makanan & Minuman", "Produk makanan dan minuman sehari-hari"),
            ("Sembako", "Kebutuhan pokok dan bahan makanan"),
            ("Perawatan Diri", "Produk kebersihan dan perawatan pribadi"),
            ("Minuman", "Berbagai jenis minuman segar dan kemasan"),
            ("Bumbu & Penyedap", "Bumbu masak dan penyedap rasa"),
            ("Bayi & Anak", "Produk untuk bayi dan anak-anak"),
            ("Pembersih", "Produk pembersih rumah tangga"),
            ("Kopi & Teh", "Kopi, teh dan minuman hangat lainnya"),
        ]

        categories = []
        if Category.objects.count() < cnt_categories:
            self.stdout.write(f"Creating {cnt_categories} categories...")
            for cat_name, cat_desc in CATEGORIES[:cnt_categories]:
                cat, created = Category.objects.get_or_create(
                    name=cat_name, defaults={"description": cat_desc}
                )
                categories.append(cat)
        else:
            categories = list(Category.objects.all())

        # helper name generators
        # curated Indonesian product names and categories
        INDONESIAN_PRODUCTS = [
            "Beras Pulen",
            "Minyak Goreng Sehat",
            "Kopi Kapal Api",
            "Teh SariWangi",
            "Mie Instan Indomie",
            "Susu Kental Manis",
            "Susu UHT",
            "Biskuit Kelapa",
            "Sabun Mandi Herbal",
            "Pasta Gigi Pepsodent",
            "Kecap Manis ABC",
            "Sambal Terasi",
            "Bumbu Instan Nasi Goreng",
            "Kopi Toraja",
            "Kopi Gayo",
            "Minyak Kayu Putih",
            "Pewangi Pakaian",
            "Susu Formula Bayi",
            "Cairan Pembersih",
            "Kopi Luwak (Kopi Spesial)",
        ]

        def product_name():
            # Prefer curated Indonesian list
            name = random.choice(INDONESIAN_PRODUCTS)
            # If duplicates may occur, optionally append a small suffix
            if Product.objects.filter(name=name).exists():
                suffix = random.randint(1, 99)
                return f"{name} {suffix}"
            return name

        def customer_name():
            if fake:
                return fake.name()
            else:
                first = ["Andi", "Budi", "Siti", "Dewi", "Agus", "Rina", "Wahyu", "Tri"]
                last = [
                    "Santoso",
                    "Pratama",
                    "Kurniawan",
                    "Wijaya",
                    "Saputra",
                    "Haryanto",
                ]
                return f"{random.choice(first)} {random.choice(last)}"

        def phone_number():
            if fake:
                # Faker id_ID may produce various formats; normalize to common Indonesian mobile format
                num = fake.phone_number()
                # Ensure it starts with 08; fallback to generated digits
                if num and num.strip().startswith("08"):
                    return num
                # sometimes faker returns with country code, strip non-digits
                import re

                digits = re.sub(r"\D", "", num)
                if digits.startswith("62"):
                    digits = "0" + digits[2:]
                if digits.startswith("08"):
                    return digits
                return f"08{random.randint(11111111,99999999)}"
            else:
                return f"08{random.randint(11111111,99999999)}"

        # create products
        products = list(Product.objects.all())
        if len(products) < cnt_products:
            self.stdout.write(f"Creating {cnt_products - len(products)} products...")
            for i in range(cnt_products - len(products)):
                name = product_name()
                price = Decimal(random.randint(5000, 150000))
                stock = random.randint(0, 500)
                # assign random category
                category = random.choice(categories) if categories else None
                # create an Indonesian description when possible
                if fake:
                    desc = fake.sentence(nb_words=8)
                else:
                    desc_options = [
                        "Produk berkualitas dengan harga terjangkau.",
                        "Cocok untuk kebutuhan sehari-hari keluarga Indonesia.",
                        "Terbuat dari bahan pilihan, aman dan halal.",
                        "Produk populer dan banyak diminati.",
                    ]
                    desc = random.choice(desc_options)
                # add a placeholder image via picsum using index to vary images
                seed = i
                try:
                    img_url = f"https://picsum.photos/seed/{seed}/320/240"
                except Exception:
                    img_url = ""
                p = Product.objects.create(
                    name=name,
                    category=category,
                    price=price,
                    stock=stock,
                    description=desc,
                    image_url=img_url,
                )
                products.append(p)

        # create customers
        customers = list(Customer.objects.all())
        if len(customers) < cnt_customers:
            self.stdout.write(f"Creating {cnt_customers - len(customers)} customers...")
            for i in range(cnt_customers - len(customers)):
                name = customer_name()
                phone = phone_number()
                Customer.objects.create(name=name, phone=phone)

        products = list(Product.objects.all())
        customers = list(Customer.objects.all())

        # create orders
        existing_orders = Order.objects.count()
        self.stdout.write(f"Creating {max(0, cnt_orders - existing_orders)} orders...")
        for i in range(max(0, cnt_orders - existing_orders)):
            cust = random.choice(customers)
            num_items = random.randint(1, 4)
            chosen = random.sample(products, min(num_items, len(products)))
            total = Decimal(0)
            order = Order.objects.create(customer=cust, total_price=Decimal(0))
            for prod in chosen:
                qty = random.randint(1, min(5, prod.stock + 5))
                price = prod.price
                # randomly apply discount (30% chance, 5-25% off)
                discount = Decimal(0)
                if random.random() < 0.3:
                    discount = Decimal(random.randint(5, 25))

                OrderItem.objects.create(
                    order=order,
                    product=prod,
                    quantity=qty,
                    price=price,
                    discount_percent=discount,
                )
                subtotal = price * qty * (1 - discount / 100)
                total += subtotal
                # optionally decrease stock but don't make negative
                if prod.stock is not None:
                    prod.stock = max(0, prod.stock - qty)
                    prod.save(update_fields=["stock"])
            order.total_price = total
            order.save(update_fields=["total_price"])

        self.stdout.write(self.style.SUCCESS("Seeding complete."))

        self.stdout.write("Summary:")
        self.stdout.write(f" Categories: {Category.objects.count()}")
        self.stdout.write(f" Products: {Product.objects.count()}")
        self.stdout.write(f" Customers: {Customer.objects.count()}")
        self.stdout.write(f" Orders: {Order.objects.count()}")
