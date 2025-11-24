from decimal import Decimal
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate dummy products and customers using Faker."

    def add_arguments(self, parser):
        parser.add_argument(
            "--products", type=int, default=50, help="Number of products to create"
        )
        parser.add_argument(
            "--customers", type=int, default=50, help="Number of customers to create"
        )
        parser.add_argument(
            "--locale", type=str, default="id_ID", help="Faker locale (default: id_ID)"
        )
        parser.add_argument(
            "--min-price", type=float, default=1000.0, help="Minimum product price"
        )
        parser.add_argument(
            "--max-price", type=float, default=50000.0, help="Maximum product price"
        )
        parser.add_argument(
            "--max-stock", type=int, default=200, help="Maximum stock for products"
        )

    def handle(self, *args, **options):
        try:
            from faker import Faker
        except ImportError:
            self.stdout.write(
                self.style.ERROR(
                    "Faker is not installed. Run 'pip install Faker' or install from requirements.txt."
                )
            )
            return

        faker = Faker(options.get("locale") or "id_ID")
        Faker.seed(0)

        from pos.models import Product, Customer
        import random

        prod_count = options["products"]
        cust_count = options["customers"]
        min_price = options["min_price"]
        max_price = options["max_price"]
        max_stock = options["max_stock"]

        created_p = 0
        created_c = 0

        # Create products
        names = set()
        for i in range(prod_count):
            # make a reasonably unique product name
            name = f"{faker.word().capitalize()} {faker.word().capitalize()}"
            # avoid duplicates
            while name in names:
                name = f"{faker.word().capitalize()} {faker.word().capitalize()}"
            names.add(name)

            price = Decimal(str(round(random.uniform(min_price, max_price), 2)))
            stock = random.randint(0, max_stock)
            description = faker.sentence(nb_words=6)

            obj, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    "price": price,
                    "stock": stock,
                    "description": description,
                },
            )
            if created:
                created_p += 1

        # Create customers
        for i in range(cust_count):
            name = faker.name()
            phone = faker.phone_number()
            address = faker.address().replace("\n", ", ")
            obj, created = Customer.objects.update_or_create(
                name=name,
                defaults={"phone": phone, "address": address},
            )
            if created:
                created_c += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created/updated {prod_count} products ({created_p} new)"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created/updated {cust_count} customers ({created_c} new)"
            )
        )
